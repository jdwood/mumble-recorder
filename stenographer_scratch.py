#!/usr/bin/python3
# This bot sends any sound it receives back to where it has come from.
# WARNING! Don't put two bots in the same place!

import time

import psycopg2 as pg

import speech_recognition as sr

from pymumble_py3 import Mumble
from pymumble_py3.callbacks import PYMUMBLE_CLBK_SOUNDRECEIVED as PCS

PCM_STREAM_WRITER = open("raw_pcm.dat", "wb")
def sound_received_handler(_user, soundchunk):
    PCM_STREAM_WRITER.write(soundchunk.pcm)

PCM_STREAM_READER = open("raw_pcm.dat", "rb")

mumble = Mumble("localhost", "Stenographer")
mumble.callbacks.set_callback(PCS, sound_received_handler)
mumble.set_receive_sound(1)  # we want to receive sound
mumble.start()

speech_rec = sr.Recognizer()

db = pg.connect("postgresql://postgres:postgres@localhost/mumble_stenographer")

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
        audio = sr.AudioData(frame_data=all_chunks, sample_rate=48000, sample_width=2)
        try:
            stt_result = speech_rec.recognize_google(audio)
            print(stt_result)

            mumble.my_channel().send_text_message(stt_result)

            with db.cursor() as cur:
                cur.execute("INSERT INTO text_to_speech (recording, text) VALUES (%(p1)s,%(p2)s)", {"p1": all_chunks, "p2": stt_result})
            db.commit()
        except Exception as e:
            print("Got error: {}".format(e))
    previous_chunk = pcm_chunk
        
