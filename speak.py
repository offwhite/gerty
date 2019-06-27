import sys
import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.fiona')
    return engine

def say(string):
    print('[INFO SAYING] '+string)
    engine.say(string)
    engine.runAndWait() #blocks

engine = init_engine()
say(str(sys.argv[1]))
