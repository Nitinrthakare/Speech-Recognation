import speech_recognition as sr
from time import ctime
import webbrowser
import time
from gtts import gTTS
import os
import random
import playsound as p

# Initialize recognizer
r = sr.Recognizer()

def record_audio(prompt=None):
    """Record audio from the microphone and return the recognized text."""
    with sr.Microphone() as source:
        if prompt:
            alexa_speak(prompt)
        r.adjust_for_ambient_noise(source)  # Improve accuracy by adjusting for ambient noise
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            alexa_speak('Sorry, I did not understand the audio.')
        except sr.RequestError:
            alexa_speak('Sorry, my speech service is down.')
        return ""

def alexa_speak(text):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang='en')
    audio_file = f'audio-{random.randint(1, 1000000)}.mp3'
    tts.save(audio_file)
    p.playsound(audio_file)
    os.remove(audio_file)
    print(text)

def respond(voice_data):
    """Respond to the recognized voice command."""
    if 'what is your name' in voice_data:
        alexa_speak("My name is Nitin")
    elif 'what time is it' in voice_data:
        alexa_speak(ctime())
    elif 'search' in voice_data:
        search_query = record_audio("What do you want to search for?")
        if search_query:
            url = f'https://google.com/search?q={search_query}'
            webbrowser.open(url)
            alexa_speak(f"Here is what I found for {search_query}")
    elif 'find location' in voice_data:
        location = record_audio("What is the location?")
        if location:
            url = f'https://google.nl/maps/place/{location}/'
            webbrowser.open(url)
            alexa_speak(f"Here is the location of {location}")
    elif 'exit' in voice_data:
        alexa_speak("Goodbye!")
        exit()

def main():
    """Main function to run the voice assistant."""
    time.sleep(1)
    alexa_speak("How can I help you?")
    while True:
        voice_data = record_audio()
        if voice_data:
            respond(voice_data)

if __name__ == "__main__":
    main()
