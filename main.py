import speech_recognition as sr
import pyttsx3
import pywhatkit

r = sr.Recognizer
engine = pyttsx3.init()
bot_name = ['megaman', 'mega man']


def talk(text):
    engine.say(text)
    engine.runAndWait()


while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()

            if 'megaman' or 'mega man' in text:
                for x in bot_name:
                    text = text.replace(x, '')
            if 'play' in text:
                song = text.replace('play', '')
                talk('playing ' + song)
                pywhatkit.playonyt(song)

    except:
        r = sr.Recognizer()
        continue
