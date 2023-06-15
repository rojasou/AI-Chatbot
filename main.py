import speech_recognition as sr
import pyttsx3

r = sr.Recognizer
engine = pyttsx3.init()
while True:
    try:
        with sr.Microphone() as source:
            print("Say something")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()

            print(f"Recognized text:{text}")
            if 'megaman' in text:
                text = text.replace('megaman', '')
                print(text)

    except:
        print("No audio detected")
        r = sr.Recognizer()
        continue
