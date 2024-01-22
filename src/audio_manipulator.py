from gtts import gTTS
from playsound import playsound

import os,sys
import time

import queue, threading
import sounddevice as sd
import soundfile as sf



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
    playsound(resource_path('resources/topic.mp3'))
    t2 = time.time()
    print(t2-t)

def prepare_tts():
    t = time.time()
    playsound(resource_path('resources/prepare.mp3'))
    t2 = time.time()
    print(t2 - t)

def speaknow_tts():
    t = time.time()
    playsound(resource_path('resources/speaknow.mp3'))
    t2 = time.time()
    print(t2 - t)


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


def start():
    global recorder
    global recording
    recording = True
    recorder = threading.Thread(target=complicated_record)
    print('start recording')
    recorder.start()


def stop():
    global recorder
    global recording
    recording = False
    recorder.join()
    print('stop recording')

if __name__=="__main__":
    start()
    time.sleep(10)
    stop()

    topic_tts("Would you prefer to work in a team or work alone on a project? Include details and explanation.")
    prepare_tts()
    speaknow_tts()