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
        st.markdown("<h1 style='font-style: italic;padding-top:0px;margin-top:0px; color: #00000;'>Hey Bird👋 </h1>", unsafe_allow_html=True)
        st.write("")

        st.subheader("ABOUT:")
        st.markdown("<span style='font-size: 20px;'>Summ-Bird is a powerful Python-based project that brings a touch of magic to Twitter data analysis. "
                    "With Summ-Bird, you can extract vital information and generate concise summaries from multiple tweets "
                    "of your favorite Twitter handles. It's time to unlock the secrets of the avian world!"
                    "</span>",
                    unsafe_allow_html=True)

        st.write("")
        st.write("")

        st.subheader("HOW TO USE: ")
        st.markdown("<p style='cursor: default; font-size: 20px;'>1. Enter the Twitter handle you want to know about."
                    "<br>2. Drag and select how many tweets you want a summary of."
                    "<br>3. Click Know."
                    "<br>4. Voila! Your summary is here!"
                    "<br>5. To view Additional Materials, select a keyword from the SelectBox.</p>",
                    unsafe_allow_html=True)
        col1,col2,col3= st.columns([1,5,1])
        with col2:
            lottie_animation_1 = "https://assets10.lottiefiles.com/packages/lf20_uui8d4hv.json"
            lottie_anime_json = load_lottie_url(lottie_animation_1)
            st_lottie(lottie_anime_json, key="hello")

