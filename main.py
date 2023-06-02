import streamlit as st
st.set_page_config(page_title="Summ-Bird", page_icon="img.png")
from func import query, start_haystack,get_data
import requests
from hidden import api_key

# @st.cache_resource
# def load_lottie_url(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

col1,col2= st.columns([1,4])
with col1:
    st.image("img_1.png",width=100)
with col2:
    st.title("Summ-Bird")
st.header("Wanna Know what's the bird been tweeting about?")
st.write("")
st.markdown("<h5 style= padding-bottom:0px; margin-bottom: 0px>Enter the twitter handle:</h5>",unsafe_allow_html=True)
username = st.text_input("")
st.write("")
st.write("")
st.markdown("<h5 style= padding-bottom:0px; margin-bottom: 0px>How many tweets do you want to summarize?</h5>",unsafe_allow_html=True)
no_tweets = st.slider("",1,20)
button=st.button("Know")
if st.session_state.get('button') != True:
    st.session_state['button'] = button
if st.session_state['button'] == True and username:
    try:
        with st.spinner("Loading⏳....."):
            tweets = get_data(username,no_tweets)
            prompt, template = start_haystack(api_key,tweets)
            results = query(prompt, template)
            ans=results[0]
            st.markdown(f"<h4 style='font-family: Roboto; font-weight: normal;'>{ans}</h4>", unsafe_allow_html=True)
            show=st.button("Show Tweets")
            if show:
                st.session_state['show']= True
                st.markdown(f"<h4 style='font-family: Roboto; font-weight: normal;'>{tweets}</h4>", unsafe_allow_html=True)

    except Exception as e:
        st.write(e)
        st.write("Kindly reduce the no. of tweets to summarize")
elif button and not username:
    st.warning("Please enter a twitter handle")