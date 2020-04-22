#!/usr/bin/python3
# This bot sends any sound it receives back to where it has come from.
# WARNING! Don't put two bots in the same place!
import os 

import time

import psycopg2 as pg

from pymumble.pymumble_py3 import Mumble
from pymumble.pymumble_py3.callbacks import PYMUMBLE_CLBK_SOUNDRECEIVED as PCS

PCM_STREAM_WRITER = open("raw_pcm.dat", "wb")
def sound_received_handler(_user, soundchunk):
    PCM_STREAM_WRITER.write(soundchunk.pcm)

PCM_STREAM_READER = open("raw_pcm.dat", "rb")

mumble = Mumble(
    os.environ["MUMBLE_SERVER"].strip(), 
    os.environ["MUMBLE_USER"].strip(),
    port=int(os.environ.get("MUMBLE_PORT", None)), 
    password=os.environ["MUMBLE_PASSWORD"].strip())

mumble.callbacks.set_callback(PCS, sound_received_handler)
mumble.set_receive_sound(1)  # we want to receive sound
mumble.start()

db = pg.connect(os.environ["DB_URL"].strip())

previous_chunk = None
pcm_chunks = []
while 1:
    time.sleep(0.5)

    pcm_chunk = PCM_STREAM_READER.read()
    if pcm_chunk:
        pcm_chunks.append(pcm_chunk)
    
    if previous_chunk and not pcm_chunk:
        all_chunks = bytearray()
        for chunk in pcm_chunks:
            all_chunks += chunk
        pcm_chunks.clear()

        try:
            with db.cursor() as cur:
                cur.execute("INSERT INTO sound_chunks (pcm_chunk) VALUES (%(p1)s)", {"p1": all_chunks})
            db.commit()
        except Exception as e:
            print("Got error: {}".format(e))
             
    previous_chunk = pcm_chunk
        
