import os
import requests
import pywhatkit
import datetime
from datetime import date
import pyttsx3 #pip install pyttsx3
import time
import pyaudio #pip install pyaudio
import speech_recognition as sr #pip install SpeechRecognition
import PySimpleGUI as sg
import json

#TODO: Fix Window Status, add stuff with names

print("Imports completed")

listener = sr.Recognizer()
engine = pyttsx3.init()

global status
global getid
status = "Ok!"

idstatus = open("config.json", "r")
tmpidstatus = idstatus.read()
idstatus.close()
idstatus2 = json.loads(tmpidstatus)
idstatus = idstatus2["getid"]
getid = str(idstatus)

def say(text):
    engine.say(text)
    engine.runAndWait()

def get_command():
    update_window()
    try:
        if(getid == True):
            for index, name in enumerate(sr.Microphone.list_microphone_names()): #main pc should be 50
                print(f'{index}, {name}')
        microphone = sr.Microphone(device_index=51)
        with microphone as source:
            print("Waiting for command...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            print("Got command:" + command)

    except Exception as e:
        print(str(e))
        status = "Failed Command"
        update_window()
        gpterror = "The following is a python error, please explain this error in one sentence.\n" + str(e) 
        #make request to gpt to summarize error
        command = ""
        say(command)
    return command

def run():
    action = get_command()
    update_window()
    if ('hey robot' in action or 'hey chatbot' in action or 'hey gpt' in action or 'hey chatgpt' in action):
        if 'play' in action:
            #send message to gpt to get song name from command
            songname = ""
            song = songname
            say('Now playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in action or 'date' in action or 'day' in action:
            time = datetime.datetime.now().strftime('%I:%M %p')
            current_time = datetime.datetime.now()
            say('The current time is ' + time)
            say(current_time.year + ", " + current_time.month + ", " + current_time.day)
        else:
            #send message to gpt to get response
            response = ""
            say(response)

def update_window():
    sg.ChangeLookAndFeel('DarkAmber')
    layout = [[sg.Text("GPT Home is running!")],
              [sg.Text('Status: ' + status)],
              [sg.Text('© 2023 Robby V2')]]
    window = sg.Window("GPT Home", icon='logo.ico').Layout(layout)

while True:
    sg.ChangeLookAndFeel('DarkAmber')
    layout = [[sg.Text("GPT Home is running!")],
              [sg.Text('Status: ' + status)],
              [sg.Text('© 2023 Robby V2')]]
    window = sg.Window("GPT Home", icon='logo.ico').Layout(layout)
    window.Read() 
    run()
