from .base_command import BaseCommand
import psycopg2
import os
import time

class PlaybackConvo(BaseCommand):

    DEFAULT_LIMIT = 10

    @staticmethod
    def name():
        return "playback-convo"

    # For now, just check that a single arg exists
    def _validate(self):
        validity = True
        if len(self.args) < 2:
            validity =  False
        return validity

    # Play latest sound generated by the user
    def _execute(self):
        if len(self.args) == 3:
            try:
                limit = int(self.args[2])
            except ValueError:
                limit = self.DEFAULT_LIMIT
        else:
            limit = self.DEFAULT_LIMIT
            
        with psycopg2.connect(os.environ["DB_URL"].strip()) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    WITH target_chunk AS (
                        SELECT id
                        FROM (
                            SELECT id, ROW_NUMBER() OVER (PARTITION BY username ORDER BY created_at DESC) as rnum
                            FROM sound_chunks
                            WHERE lower(username) = lower(%(username)s)
                            LIMIT %(offset)s
                        ) pcm
                        WHERE rnum = %(offset)s
                    )
                    SELECT pcm_chunk
                    FROM sound_chunks
                    WHERE id >= (SELECT id FROM target_chunk)
                    ORDER BY created_at
                    LIMIT %(limit)s
                """, {"username": self.args[0], "offset": self.args[1], "limit": limit})
                sound_chunks = cur.fetchall()
                print(cur.query)
        conn.close()

        for pcm in sound_chunks:
            sound = bytes(pcm[0])
            self.mumble.sound_output.add_sound(sound)