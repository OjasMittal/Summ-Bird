#import requests
#import datetime
"""
# Define search parameters
search_engine_id = "your engine id"
api_key = "your api key (hidden)"
query = "india-nepal relations"

# Define API endpoint and parameters
url = "your url"
params = {
    "cx": search_engine_id,
    "key": api_key,
    "q": query,
    "sort": "date:r:20100101:{}".format(datetime.date.today().strftime("%Y%m%d")),
    "num": 10,
    "fields": "items(title,link,pubDate)"
}

# Make API request and retrieve results
response = requests.get(url, params=params)
result = response.json()

# Check if response contains any errors
if "error" in result:
    error_message = result["error"]["message"]
    print(f"API Error: {error_message}")
else:
    # Print titles and links of each article
    if "items" in result:
        for item in result["items"]:
            print(item["title"])
            print(item["link"])
            if "pubDate" in item:
                print(item["pubDate"])
            print()
    else:
        print("No items found in the response.")

print(result)
"""


from googleapiclient.discovery import build

# Set up your API key and search engine ID
API_KEY = 'your api key (hidden)'
SEARCH_ENGINE_ID = 'your engine id'

def get_latest_articles(query):
    # Create a service object using your API key
    service = build('customsearch', 'v1', developerKey=API_KEY)

    # Make the search request
    res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=5).execute()

    # Retrieve the search results
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

# Example usage
query = 'india-nepal war'
latest_articles = get_latest_articles(query)

# Print the results
for article in latest_articles:
    print('Title:', article['title'])
    print('Link:', article['link'])
    print('Snippet:', article['snippet'])
    print()
