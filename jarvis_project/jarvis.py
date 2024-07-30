import speech_recognition as sr
import webbrowser
import pyttsx3 
import music_library
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os


# Create an object of speech recognition
Recognizer = sr.Recognizer()

# Initialize the pyttsx3
engine = pyttsx3.init()

# my api for news
newsapi = "YOUR_NEWS_API_KEY"

def aiProcess(command):
    client = OpenAI(api_key="YOUR_OPENAI_API_KEY",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def speak_say(text):
   # Initialize the TTS engine
    engine = pyttsx3.init()

    # voices = engine.getProperty('voices')

    # def change_voice(indx, rate = 120, volume = 1.0):

    #     idname = voices[ indx ].id
    #     engine.setProperty('voice', idname)
    #     engine.setProperty('rate', rate)
    #     engine.setProperty('volume', volume)
    #     engine.runAndWait()


    # # enunciate all available names
    # for indx, v in enumerate(voices):
    #     change_voice(indx, rate = 140, volume = 1)

    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]  # Ensure the entire song name is captured
        link = music_library.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?q=trump&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # Let OpenAI handle the request
        output = aiProcess("what is chatgpt")
        speak(output) 
        print(output)

if __name__ == "__main__":
    speak("Initializing Jarvis... ")


    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = Recognizer.listen(source, timeout=5, phrase_time_limit=3)  # Increased time limits for better recognition

            word = Recognizer.recognize_google(audio)   # it will be recognize the word 
            

            if word.lower() == 'jarvis':
                speak("Yes")

                with sr.Microphone() as source:
                    print("Jarvis Activated.... Listening for command...")
                    audio = Recognizer.listen(source, timeout=5, phrase_time_limit=3)  

                try:
                    command = Recognizer.recognize_google(audio)

                except sr.UnknownValueError:
                    speak("Sorry, I did not understand the command.")
                    continue

                except sr.RequestError as e:
                    speak(f"Could not request results from Google Speech Recognition service; {e}")
                    continue

                processCommand(command)

        except Exception as e:
            print(f"Unexpected error: {e}")
