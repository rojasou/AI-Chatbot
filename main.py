from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request
from playsound import playsound
import requests
import os

load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")


def get_response_from_ai(human_input):
    template = """I want you to act as an interviewer. I will be the candidate and you will ask me the interview 
    questions for the position position. I want you to only reply as the interviewer. Do not write all the conservation 
    at once. I want you to only do the interview with me. Ask me the questions and wait for my answers. Do not write 
    explanations. Ask me the questions one by one like an interviewer does and wait for my answers. My first sentence is 
    "Hi"

    {history}
    User: {human_input}
    Interviewer:
    """

    prompt = PromptTemplate(
        input_variables={"history", "human_input"},
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0.2),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
    )

    output = chatgpt_chain.predict(human_input=human_input)

    return output


def get_voice_message(message):
    payload = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application.json"
    }

    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM?optimize_streaming_latency=0", json=payload,
        headers=headers)
    if response.status_code == 200 and response.content:
        with open("audio.mp3", "wb") as f:
            f.write(response.content)
        playsound("audio.mp3")
        return response.content


# Web GUI
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/send_message', methods=['POST'])
def send_message():
    human_input = request.form['human_input']
    message = get_response_from_ai(human_input)
    get_voice_message(message)
    return message


if __name__ == "__main__":
    app.run(debug=True)
