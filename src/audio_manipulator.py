from gtts import gTTS
import pygame

import os,sys
import time

import queue, threading
import sounddevice as sd
import soundfile as sf

import tkinter as tk
import speech_recognition as sr

r = sr.Recognizer()

pygame.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def topic_tts(topic):
    tts = gTTS(
        text=topic,
        lang='en', slow=False
    )
    tts.save(resource_path('resources/topic.mp3'))

    t = time.time()
    pygame.mixer.music.load(resource_path('resources/topic.mp3'))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    t2 = time.time()
    print(t2-t)

def prepare_tts():
    t = time.time()
    pygame.mixer.music.load(resource_path('resources/prepare.mp3'))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    t2 = time.time()
    print(t2 - t)

def speaknow_tts():
    while pygame.mixer.music.get_busy():
        pass
    t = time.time()
    pygame.mixer.music.load(resource_path('resources/speaknow.mp3'))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    t2 = time.time()
    print(t2 - t)

def beep():
    while pygame.mixer.music.get_busy():
        pass
    t = time.time()
    pygame.mixer.music.load(resource_path('resources/beep.mp3'))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    t2 = time.time()
    print(t2 - t)

def delay(seconds, intvar = None):
    flag = 0
    if isinstance(intvar, tk.IntVar):
        flag = 1
    for i in range(seconds):
        time.sleep(1)
        if flag:
            intvar.set(intvar.get() - 1)



q = queue.Queue()
recorder = False
recording = False


def complicated_record():
    with sf.SoundFile(resource_path('resources/record.wav'), mode='w', samplerate=16000, subtype='PCM_16', channels=1) as file:
        with sd.InputStream(samplerate=16000, dtype='int16', channels=1, callback=complicated_save):
            while recording:
                file.write(q.get())


def complicated_save(indata, frames, time, status):
    q.put(indata.copy())


def record_start():
    global recorder
    global recording
    recording = True
    recorder = threading.Thread(target=complicated_record)
    print('start recording')
    recorder.start()


def record_stop():
    global recorder
    global recording
    recording = False
    recorder.join()
    print('stop recording')

def speaking_to_text():
    with sr.AudioFile(resource_path('resources/record.wav')) as source:
        audio = r.record(source, duration=120)

    speech_text = r.recognize_google(audio_data=audio)

    print(speech_text)

    return speech_text

if __name__=="__main__":
    """
    record_start()
    time.sleep(10)
    record_stop()

    speaking_to_text()
    """
    topic_tts("Would you prefer to work in a team or work alone on a project? Include details and explanation.")
    prepare_tts()
    speaknow_tts()