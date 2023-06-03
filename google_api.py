from googleapiclient.discovery import build
API_KEY = 'AIzaSyDJuQhr_kZWartlIic-qV4LMB4bNoASzA4'
SEARCH_ENGINE_ID = 'e77aadef9bb7b49c1'

def get_latest_articles(query):
    service = build('customsearch', 'v1', developerKey=API_KEY)
    word="Tweets about"+query
    res = service.cse().list(q=word, cx=SEARCH_ENGINE_ID, num=5).execute()
    articles = []
    if 'items' in res:
        for item in res['items']:
            article = {
                'title': item['title'],
                'link': item['link'],
                'snippet': item['snippet']
            }
            articles.append(article)

    return articles

if __name__ == '__main__':
    query = """These topics include film critics, the platform itself, " 
            "cows and climate change, and France.The profile has tweeted about" 
            " film critics in a sarcastic tone, such as Audience score is what matters, as film critics" 
            " are terrified of being ostracized for wrong-think" (@MattWalshBlog).The profile has also been tweeting about the platform, often in a humorous way, such as 
            "This platform honestly gives me more laughs per day than everything else combined!" (@cb_doge)."""
    latest_articles = get_latest_articles(query)

    for article in latest_articles:
        print('Title:', article['title'])
        print('Link:', article['link'])
        print('Snippet:', article['snippet'])
        print()