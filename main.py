import streamlit as st
from func import query, start_haystack,get_data
import requests
from side import sidebar
from streamlit_lottie import st_lottie
from google_api import get_latest_articles

st.set_page_config(page_title="Summ-Bird", page_icon="img.png",layout="wide")
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def clear_submit():
    st.cache_data.clear()


hide_menu_style="""
<style>
footer{visibility:hidden;}
</style>
"""
st.markdown(hide_menu_style,unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)
coll1,coll2,coll3= st.columns([1,4,1])
with coll2:
    sidebar()
    col1,col2= st.columns([2,4])
    with col1:
        lottie_animation_1 = "https://assets1.lottiefiles.com/packages/lf20_5mhyg2hz.json"
        lottie_anime_json = load_lottie_url(lottie_animation_1)
        st_lottie(lottie_anime_json, key="logo")
    with col2:
        st.markdown("<h1 style='padding-top: 1.7em;'>Summ-<span style='color: #26C3E2;'>Bird</span></h1>", unsafe_allow_html=True)

    st.markdown("<h2 style= padding-top:0px;>Wanna Know what's the bird been tweeting about?</h2>",unsafe_allow_html=True)
    st.write("")
    st.markdown("<h5 style= padding-bottom:0px; margin-bottom: 0px>Enter the twitter handle:</h5>",unsafe_allow_html=True)

    username = st.text_input("",on_change=clear_submit())
    st.markdown(
        """
        <style>
        input {
            font-size: 1.3rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.write("")
    st.markdown("<h5 style= padding-bottom:0px; margin-bottom: 0px>How many tweets do you want to summarize?</h5>",unsafe_allow_html=True)
    no_tweets = st.slider("",1,20)
    api_key=st.secrets["api_key"]

    @st.cache_data(show_spinner=False)
    def compute():
        try:
            with st.spinner("Fetching⏳....."):
                tweets, lst = get_data(username, no_tweets)
                prompt, template = start_haystack(api_key, tweets)
                results = query(prompt, template)
                ans = results[0]
                st.markdown(
                    f"<h4 style='font-family: Roboto; font-weight: normal;'>@{username} has been tweeting about:</h4>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<h4 style='font-family: Lato; border: 2px solid #26C3E2; padding: 15px; font-weight: normal;'>{ans}</h4>",
                    unsafe_allow_html=True)
                st.write("")
                st.write("")
                st.markdown(f"<h3>Source Tweets:</h3>", unsafe_allow_html=True)
                for i in lst:
                    st.markdown(f"<h5 style='font-family: Chirp; font-weight: normal;'>{i}</h5>",
                                unsafe_allow_html=True)
                    st.divider()

        except Exception as e:
            st.write(e)
            st.write("Kindly reduce the no. of tweets to summarize")
        return ans

    if "button" not in st.session_state:
        st.session_state["button"] = False
    flag=False


    button=st.button("Know")
    if st.session_state.get('button') != True:
        st.session_state['button'] = button
    if st.session_state['button'] == True and username:
        flag=True
        ans=compute()

    if flag:
        st.markdown(f"<h3>Do you want to know more about a particular topic?</h3>", unsafe_allow_html=True)
        addon=st.text_input("Enter a keyword from the summary")

        check=st.checkbox("Explore")
        if check:
            if addon and addon in ans:
                articles=get_latest_articles(addon)
                st.write("")
                st.markdown(f"<h3>Tweets related to {addon}:</h3>", unsafe_allow_html=True)
                for article in articles:
                    st.write('<span style="font-size: 20px;">Title:</span>',
                             f'<span style="font-size: 20px;">{article["title"]}</span>', unsafe_allow_html=True)
                    st.write('<span style="font-size: 20px;">Link:</span>',
                             f'<span style="font-size: 20px;">{article["link"]}</span>', unsafe_allow_html=True)
                    st.write('<span style="font-size: 20px;">Snippet:</span>',
                             f'<span style="font-size: 20px;">{article["snippet"]}</span>', unsafe_allow_html=True)
                    st.divider()
    elif button and not username:
        st.warning("Please enter a twitter handle")
