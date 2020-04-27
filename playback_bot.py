#!/usr/bin/python3
# This bot sends any sound it receives back to where it has come from.
# WARNING! Don't put two bots in the same place!
import os 

import time

import psycopg2 as pg
from functools import partial 

from pymumble.pymumble_py3 import Mumble
from pymumble.pymumble_py3.callbacks import PYMUMBLE_CLBK_SOUNDRECEIVED as PCS
from pymumble.pymumble_py3.callbacks import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED as PCT

from bots.commands.command_listener import CommandListener
from bots.commands.playback_command import PlaybackCommand


def sound_received_handler(pcm_stream, _user, soundchunk):
    pcm_stream.write(soundchunk.pcm)

def text_received_handler(cmd_listener, event):
    cmd = cmd_listener.create_command(event.message)
    if cmd:
        cmd.execute()

PCM_STREAM_WRITER = open("raw_pcm.pipe", "wb")

mumble = Mumble(
    os.environ["MUMBLE_SERVER"].strip(), 
    os.environ["MUMBLE_USER"].strip(),
    port=int(os.environ.get("MUMBLE_PORT", None)), 
    password=os.environ["MUMBLE_PASSWORD"].strip())

mumble.callbacks.set_callback(PCS, partial(sound_received_handler, PCM_STREAM_WRITER))
mumble.callbacks.set_callback(PCT, partial(text_received_handler, CommandListener(commands=[PlaybackCommand])))
mumble.set_receive_sound(1)  # we want to receive sound
mumble.start()

db = pg.connect(os.environ["DB_URL"].strip())

PCM_STREAM_READER = open("raw_pcm.pipe", "rb")

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
        
