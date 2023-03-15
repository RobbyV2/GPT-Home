import os
import requests
import pywhatkit
import datetime
from datetime import date
import pyttsx3 #pip install pyttsx3
import time
import pyaudio #pip install pyaudio
import speech_recognition as sr #pip install SpeechRecognition
import sys
import PySimpleGUI as sg
import json
import openai
import asyncio

#TODO: Fix Window Status, add stuff with names, show debug console
#IMPORTANT: Remove api key before making push

print("Imports completed")

listener = sr.Recognizer()
engine = pyttsx3.init()

global status
global getid
global apikey
status = "Ok!"

idstatus = open("config.json", "r")
tmpidstatus = idstatus.read()
idstatus.close()
idstatus2 = json.loads(tmpidstatus)
idstatus = idstatus2["getid"]
getid = str(idstatus)

key = open("config.json", "r")
tmpkey = key.read()
key.close()
key2 = json.loads(tmpkey)
key = key2["apikey"]
apikey = str(key)

openai.api_key = apikey

def generate(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant made to clone alexa or google home. Your name is GPT. If anyone asks you your name, it is GPT."},
            {"role": "system", "content": "The home assistant part of you is made by a person named Robby. You have two creators, OpenAI and Robby."},
            {"role": "system", "content": "If someone asks you to only do something, you must do it."},
            {"role": "system", "content": "You are GPT, a large language model trained by OpenAI. Answer as concisely as possible."},
            {"role": "system", "content": "Any of your answers should be at most 15 words. Your responses should be complete sentences rewording the original question. They should also be straight to the point and use non-complex words."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def say(text):
    engine.say(text)
    engine.runAndWait()

async def get_command():
    #update_window()
    #try:
        if(getid == True):
            for index, name in enumerate(sr.Microphone.list_microphone_names()): #main pc should be 51
                print(f'{index}, {name}')
        microphone = sr.Microphone(device_index=51)
        with microphone as source:
            print("Waiting for command...")
            voice = listener.listen(source)
            try:
                command = listener.recognize_google(voice)
            except:
                return
            print("Got command: " + command)

   # except Exception as e:
   #     print(str(e))
   #     status = "Failed Command"
   #    update_window()
   #     print(e)
   #     gpterror = "The following text is a python error, please explain this error in one very short sentence.\n" + str(e) 
   #     c = generate(gpterror)
   #     command = c
   #     say(c)
        return command

def run():
    action = asyncio.run(get_command())
    #update_window()
    print("Started Run")
    if ('hey' in str(action).lower() or 'hello' in str(action).lower()or 'ok' in str(action).lower() or 'gpt' in str(action).lower()):
        if 'play' in str(action).lower() or 'song' in str(action).lower():
            print("Started Play")
            gptsong = "Please only tell me the name of the song in the following text. Do not include The song you requested or any other text apart from the song name.\n" + action
            say("Sending Request...")
            c = generate(gptsong)
            say(c)
            pywhatkit.playonyt(c)
        elif 'time' in str(action).lower() or 'date' in str(action).lower() or 'day' in str(action).lower():
            print("Started Date")
            time = datetime.datetime.now().strftime('%I:%M %p')
            current_time = datetime.datetime.now()
            say('The current time is ' + time)
            c2 = str(current_time.year) + ", " + str(current_time.month) + ", " + str(current_time.day)
            say(c2)
        else:
            print("Started Response")
            say("Sending Request...")
            c = generate(action)
            say(c)

def update_window():
    sg.ChangeLookAndFeel('DarkAmber')
    layout = [[sg.Text("GPT Home is running!")],
              #[sg.Text('Status: ' + status)],
              [sg.Text('© 2023 Robby V2')]]
    window = sg.Window("GPT Home", icon='logo.ico').Layout(layout)

async def startgui():
    while True:
        sg.ChangeLookAndFeel('DarkAmber')
        layout = [[sg.Text("GPT Home is running!")],
                #[sg.Text('Status: ' + status)],
                [sg.Button('Close')],
                [sg.Text('© 2023 Robby V2')]]
        window = sg.Window("GPT Home", icon='logo.ico').Layout(layout)
        event, values = window.read()
        count = count + 1
        if event == 'Close':
            sys.exit("Program Closed")

while True:
    #asyncio.run(startgui())
    run()
