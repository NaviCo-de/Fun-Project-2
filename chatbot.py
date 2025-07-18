import streamlit as st
import requests
from transformers import pipeline
from audiorecorder import audiorecorder

@st.dialog("Sign up")
def sign_up():
    username = st.text_input("Username")
    password = st.text_input("Password")
    if st.button("Submit"):
        st.session_state.user_account.append({username : password})
        st.rerun()

@st.dialog("Login")
def login():
    username = st.text_input("Username")
    password = st.text_input("Password")
    if st.button("Submit"):
        logged_in = False
        current_user = ""
        for item in st.session_state.user_account:
            if username in item and password == item[username]:
                logged_in = True
                current_user = username
        if logged_in:
            st.session_state.is_login = True
            st.session_state.current_user = current_user
            st.rerun()
        else:
            st.error("Username atau password salah!")

def log_out():
    st.session_state.is_login = False
def calculate_user_prompt(chat_history=[]):
    count = 0
    for chat in chat_history:
        if chat["role"] == "user":
            count += 1
    return count

# def transcript_audio(audio):
#     if len(audio) > 0:
#         audio.export("audio.wav", format="wav")
#         pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base")
#         result = pipe(audio)
#         return result['text']

if "is_login" not in st.session_state:
    st.session_state.is_login = False

if "user_account" not in st.session_state:
    st.session_state.user_account = []

if "current_user" not in st.session_state:
    st.session_state.current_user =""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
#API Key
API_KEY = "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"
MODEL = "openai/gpt-3.5-turbo"

HEADERS = {
    "Authorization" : f"Bearer {API_KEY}",
    "HTTP-Referer"  : "http://localhost:8501",
    "Content-Type"  : "application/json",
    "X-title"       : "AI Chatbot Streamlit"
}

API_URL = f"https://openrouter.ai/api/v1/chat/completions"

st.title("WELCOME TO CHATBOT!!")
st.markdown(f"Powered by 'Mistral AI'")
#Chat History


#Buat nampilin chat sebelumnya
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

input_user_text = st.chat_input("Type your message here...", disabled=not st.session_state.is_login)
# input_user_audio = audiorecorder("Click to record", "Click to stop")

# if input_user_audio:
#     text = transcript_audio(input_user_audio)
#     st.chat_message("user").markdown(text)
#     st.session_state.chat_history.append({"role" : "user", "content" : text})

#     with st.spinner("Thinking..."):
#         payload = {
#             "model" : MODEL,
#             "messages": [
#                 {"role" : "user", "content": "You are a helpful assistant"},
#                 {"role" : "user", "content": text}
#             ]
#         }

#         respon = requests.post(API_URL, headers=HEADERS, json=payload)

#         if respon.status_code == 200:
#             bot_reply = respon.json()["choices"][0]["message"]["content"]
#         else:
#             bot_reply = "Failed"

#     st.chat_message("assistant").markdown(bot_reply)
#     st.session_state.chat_history.append({"role" : "assistant", "content" : bot_reply})

if input_user_text:
    st.chat_message("user").markdown(input_user_text)
    st.session_state.chat_history.append({"role" : "user", "content" : input_user_text})

    with st.spinner("Thinking..."):
        payload = {
            "model" : MODEL,
            "messages": [
                {"role" : "user", "content": "You are a helpful assistant"},
                {"role" : "user", "content": input_user_text}
            ]
        }

        respon = requests.post(API_URL, headers=HEADERS, json=payload)

        if respon.status_code == 200:
            bot_reply = respon.json()["choices"][0]["message"]["content"]
        else:
            bot_reply = "Failed"

    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append({"role" : "assistant", "content" : bot_reply})



with st.sidebar:
    if not st.session_state.is_login:
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Login"):
                login()
        with col2:
            if st.button("Register"):
                sign_up()
    
    else:
        st.button("Log out", on_click=log_out)
        st.title(f"Hello {st.session_state.current_user}!")
        st.subheader(f"Prompt: {calculate_user_prompt(st.session_state.chat_history)}")
    