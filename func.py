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


@st.cache_resource(show_spinner=False)
def start_haystack(openai_key,tweets):
    prompt_node = PromptNode(model_name_or_path="text-davinci-003", api_key=openai_key)
    try:
        #twitter_template = PromptTemplate(name="twitter",prompt_text = f"""You are given a twitter stream belonging to a specific profile.{tweets}
                                                                  #  Answer with a summary of what they've lately been tweeting about and in what languages.
                                                                  #  You may go into some detail about what topics they tend to like tweeting about.
                                                                  #  Please also mention their overall tone, for example: positive,
                                                                  #  negative, political, sarcastic or something else.
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


    return prompt_node, twitter_template


def query(prompter, template):
    try:
        result = prompter.prompt(prompt_template=template, max_time=30,max_tokens=1500)
    except Exception as e:
        st.warning(e)
        result = ["Please make sure you are providing a correct, public twitter account"]
    return result

def get_keyword(openai_key,results):
    prompter = PromptNode(model_name_or_path="text-davinci-003", api_key=openai_key)
    summary = PromptTemplate(name="summary",
                                  prompt_text=f"""You are given a twitter stream belonging to a specific profile.{results}
                                  Give me a list of all the keywords separated by a space in the summary
                                  The output should be of format: keyword1 keyword2 keyword3  
                                  without any commas ,special characters or brackets""")
    try:
        keywords=prompter.prompt(prompt_template=summary, max_time=30)
    except Exception as e:
        print(e)
        keywords = ["Please make sure you are providing a correct, public twitter account"]
    return keywords

def Convert(string):
    li = list(string.split(" "))
    return li

if __name__ == "__main__":
    twett,lst = get_data("narendramodi",7)
    prompt,template=start_haystack(api_key,twett)
    results = query(prompt, template)
    print(results)
    summary_temp = PromptTemplate(name="summary",
                             prompt_text = f"""You are given a twitter stream belonging to a specific profile.{results}
                              Give me a python list of all the keywords in the summary""")
    keywords = get_keyword(api_key,results)
    keys=Convert(keywords[0])
    print("Keywords are:",keys)