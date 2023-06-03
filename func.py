import streamlit as st
from haystack.nodes import PromptNode, PromptTemplate
import snscrape.modules.twitter as sntwitter
import pandas as pd


api_key=st.secrets["api_key"]
@st.cache_data(show_spinner=False)
def get_data(username,tweets):
        attributes_container = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{username}').get_items()):
            if i > tweets:
                break
            attributes_container.append([tweet.date, tweet.likeCount, tweet.sourceLabel, tweet.rawContent])
        tweets_df = pd.DataFrame(attributes_container, columns=["Date Created", "Number of Likes", "Source of Tweet", "Tweets"])
        all_tweets = ""
        lst=[]
        for tweet in tweets_df["Tweets"]:
            all_tweets += tweet
            lst.append(tweet)
        return all_tweets,lst


#@st.cache(hash_funcs={"builtins.CoreBPE": lambda _: None}, show_spinner=False, allow_output_mutation=True)
@st.cache_resource(show_spinner=False)
def start_haystack(openai_key,tweets):
    prompt_node = PromptNode(model_name_or_path="text-davinci-003", api_key=openai_key)
    try:
        #twitter_template = PromptTemplate(name="twitter",prompt_text = f"""You are given a twitter stream belonging to a specific profile.{tweets}
                                                                   # Answer with a summary of what they've lately been tweeting about and in what languages.
                                                                  #  You may go into some detail about what topics they tend to like tweeting about. Please also mention their overall tone, for example: positive,
                                                                   # negative, political, sarcastic or something else.
                                                                  #  """)

        twitter_template = PromptTemplate(
            name="twitter",
            prompt_text=f"""You are given a Twitter stream belonging to a specific profile. {tweets}
                Answer with a summary of what they've lately been tweeting about and in what languages.
                You may go into some detail about what topics they tend to like tweeting about. Please also mention their overall tone, for example: positive,
                negative, political, sarcastic, or something else.

                - Summarize the main themes and subjects the profile has been tweeting about recently.
                - Provide examples of significant tweets related to each theme or subject.
                - Analyze the sentiment of the tweets. Are they mostly positive, negative, or neutral?
                - Identify any trending topics or hashtags the profile has engaged with.
                - Suggest additional sources or articles related to the topics mentioned in the summary.
                - Offer insights into the profile's tweeting style or patterns.
                - Are there any recurring phrases or keywords that stand out in their tweets?
                - Mention any notable engagements or interactions the profile has had with other users.

                For each theme or topic mentioned in the summary, provide further information or sources that can help deepen the understanding of those specific subjects.
                Additionally, suggest relevant books, research papers, or authoritative websites where the user can find more information on the trending topics mentioned in the summary.
                """
        )
    except Exception as e:
        st.write("Kindly reduce the no. of tweets to summarize")

    #st.session_state["haystack_started"] = True

    return prompt_node, twitter_template


#@st.cache(hash_funcs={"builtins.CoreBPE": lambda _: None}, show_spinner=False, allow_output_mutation=True)
def query(prompter, template):
    try:
        result = prompter.prompt(prompt_template=template, max_time=30,max_tokens=1500)
    except Exception as e:
        print(e)
        result = ["Please make sure you are providing a correct, public twitter account"]
    return result

if __name__ == "__main__":
    twett,lst = get_data("narendramodi")
    prompt,template=start_haystack(api_key,twett)

    results = query(prompt, template)
    print(results)