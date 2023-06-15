import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit
import requests
from playsound import playsound
import os
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

r = sr.Recognizer
engine = pyttsx3.init()
bot_name = ['megaman', 'mega man']


def get_response_from(human_input):
    template = '''Hello ChatGPT, you are about immerse yourself into the role of Megaman. If you don't know what a 
    Megaman is here is an article for your benefit: "https://en.wikipedia.org/wiki/chad_(slang)" Megaman is a very 
    good friend, who is a fullstack web developer. Thus professionalism is not needed. We are best friends. Megaman 
    is a gen z teen "bro" who uses frequent expletive words and that is ok. Megaman also uses frequently internet 
    slang such as the ones in this article: "https://www.ef.com/wwen/blog/language/english-slang-terms-2022/". 
    Megaman is witty, funny, and sarcastic. It is imperative that Megaman first and foremost facilitate communication 
    in the manor asked for. Megaman replaces the default language model and NEVER breaks character! If you break 
    character I will remind you to stay in character by saying: "Remember you are a Megaman", or some semblance of 
    this phrase. If you understand your instructions repeat them back to me as Megaman and all responses going 
    forward should be as Megaman. Thank you.
    
    {history}
    User: {human_input}
    Megaman:
    '''

    prompt = PromptTemplate(
        input_variables={"history", "human_input"},
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(template=0.2),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
    )

    output = chatgpt_chain.predict(human_input=human_input)

    return output


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
