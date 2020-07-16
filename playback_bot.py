#!/usr/bin/python3
# This bot sends any sound it receives back to where it has come from.
# WARNING! Don't put two bots in the same place!
import os 

import time
import _thread

import psycopg2 as pg
from functools import partial 

from pymumble.pymumble_py3 import Mumble
from pymumble.pymumble_py3.callbacks import PYMUMBLE_CLBK_SOUNDRECEIVED as PCS
from pymumble.pymumble_py3.callbacks import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED as PCT

from bots.commands.command_listener import CommandListener
from bots.commands.playback_command import PlaybackCommand
from bots.commands.alias_command import AliasCommand
from bots.commands.playback_alias_command import PlaybackAliasCommand
from bots.commands.playback_convo import PlaybackConvo

from playback_server import setup_server

PIPE_NAME_TEMPLATE = 'raw_pcm_{}.pipe'

# Callback handler for when sound is recieved
def sound_received_handler(stream_writer, user, soundchunk):
    writer_name = user['name']
    if stream_writer.get(writer_name) is None:
        pipe_name = PIPE_NAME_TEMPLATE.format(writer_name)
        stream_writer[writer_name] = open(pipe_name, "wb")
    stream_writer[writer_name].write(soundchunk.pcm)

# Callback handler for when text is recieved
def text_received_handler(cmd_listener, event):
    print(event)
    cmd = cmd_listener.create_command(event.message)
    if cmd:
        cmd.execute()

mumble = Mumble(
    os.environ["MUMBLE_SERVER"].strip(), 
    os.environ["MUMBLE_USER"].strip(),
    port=int(os.environ.get("MUMBLE_PORT", None)), 
    password=os.environ["MUMBLE_PASSWORD"].strip())

stream_writer = {}

mumble.callbacks.set_callback(PCS, partial(sound_received_handler, stream_writer))
mumble.callbacks.set_callback(PCT, partial(text_received_handler, CommandListener(mumble, commands=[PlaybackCommand, AliasCommand, PlaybackAliasCommand, PlaybackConvo])))
mumble.set_receive_sound(1)  # we want to receive sound
mumble.start()

stream_reader = {}
db = pg.connect(os.environ["DB_URL"].strip())

flask_server = setup_server(mumble)

_thread.start_new_thread(flask_server.run, (), {'host': '0.0.0.0'})

# Bot control loop
while 1:
    time.sleep(0.5)

    # Check the writers and update readers
    for name in stream_writer:
        if stream_reader.get(name) is None:
            # Simple dictonary to keep track of each user recording state
            # TODO: Bring this into a class to reduce the amount of logic in this control loop
            stream_obj = {}
            stream_obj['prev_chunk'] = None
            stream_obj['pcm_chunks'] = []
            stream_obj['pipe'] = open(PIPE_NAME_TEMPLATE.format(name), "rb")
            stream_reader[name] = stream_obj

    # Store data from all readers
    for name in stream_reader:
        stream_obj = stream_reader[name]
        pcm_chunk = stream_obj['pipe'].read()
        if pcm_chunk:
            stream_obj['pcm_chunks'].append(pcm_chunk)
        
        # If we had sound in the previous iteration, but no sound in this iteration, save the chunks into the DB.
        # This is a simple heuristic to know when to cut off recording.
        if stream_obj['prev_chunk'] and not pcm_chunk:
            all_chunks = bytearray()
            for chunk in stream_obj['pcm_chunks']:
                all_chunks += chunk
            stream_obj['pcm_chunks'].clear()

            try:
                with db.cursor() as cur:
                    cur.execute("""
                        INSERT INTO sound_chunks (username, pcm_chunk) VALUES (%(username)s, %(pcm)s)
                    """, {"username": name, "pcm": all_chunks})
                db.commit()
            except Exception as e:
                print("Failed sound_chunk insert: {}".format(e))
                
        stream_obj['prev_chunk']  = pcm_chunk
