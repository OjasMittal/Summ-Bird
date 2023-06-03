import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def sidebar():
    with st.sidebar:
        st.markdown("<h1 style='font-style: italic;padding-top:0px;margin-top:0px; color: #00000;'>Hello Bird !</h1>", unsafe_allow_html=True)
        st.write("")

        st.subheader("ABOUT:")
        st.markdown("<span style='font-size: 20px;'>"
                    "Introducing Summ-Tweet, our quirky project. "
                    "It summarizes tweets from chosen handles using Python, Twitter API, and OpenAI's GPT model. "
                    "It saves you time and keeps you in the loop!"
                    "</span>",
                    unsafe_allow_html=True)

        st.write("")
        st.write("")

        st.subheader("HOW TO USE: ")
        st.markdown("<p style='cursor: default; font-size: 20px;'>1. Enter the Twitter handle you want to know about."
                    "<br>2. Drag and select how many tweets you want a summary of."
                    "<br>3. Click Know."
                    "<br>4. Voila! Your summary is here!"
                    "<br>5. To view Tweet Sources, click on the Show Sources button.</p>",
                    unsafe_allow_html=True)
        col1,col2,col3= st.columns([1,5,1])
        with col2:
            lottie_animation_1 = "https://assets10.lottiefiles.com/packages/lf20_uui8d4hv.json"
            lottie_anime_json = load_lottie_url(lottie_animation_1)
            st_lottie(lottie_anime_json, key="hello")

