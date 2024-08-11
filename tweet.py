import tweepy
from quote import quote
import time
import random
import requests

# Twitter API credentials for multiple accounts
accounts = [
    {
        'api_key': 'your_api_key',
        'api_secret': 'your_api_secret',
        'bearer_token': r'your_bearer_token',
        'access_token': 'your_access_token',
        'access_token_secret': 'your_access_token_secret',
        'proxy': 'your_proxy'
    }
    # Add more accounts as needed
]

# List of authors to get quotes from
authors = [
    'Jasper Fforde',
    'George Orwell',
    'Mark Twain',
    'Jane Austen'
]

# Function to create a tweepy client with a specific proxy
def create_client(api_key, api_secret, bearer_token, access_token, access_token_secret, proxy=None):
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    
    if proxy:
        # Configure requests session for the client
        session = requests.Session()
        session.proxies = {'http': proxy, 'https': proxy}
        client._session = session

    return client

# Function to tweet unique quotes with a hashtag using a specific client
def tweet_unique_quote(client, author, hashtag, used_quotes, limit=5):
    try:
        results = quote(author, limit=limit)
        
        if not results:
            print(f"No quotes found for {author}.")
            return
        
        # Filter out already used quotes
        unique_quotes = [q for q in results if q["quote"] not in used_quotes]
        
        if not unique_quotes:
            print(f"All quotes for {author} have been used.")
            return
        
        # Select a random quote from the unique quotes
        selected_quote = random.choice(unique_quotes)
        quote_text = f'"{selected_quote["quote"]}" - {selected_quote["author"]} ({selected_quote["book"]})'
        tweet_text = f"{quote_text} #{hashtag}"
        
        # Create a tweet with the quote and hashtag
        client.create_tweet(text=tweet_text)
        print(f"Tweeted: {tweet_text}")
        
        # Mark this quote as used
        used_quotes.add(selected_quote["quote"])
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage for each account and author
hashtag = 'LingOrm' #hashtag
tweet_count = 300
delay_between_tweets = 120  # 2 minutes in seconds

# Track used quotes to avoid duplicates
used_quotes = set()
for _ in range(tweet_count):
    for account in accounts:
        client = create_client(
            api_key=account['api_key'],
            api_secret=account['api_secret'],
            bearer_token=account['bearer_token'],
            access_token=account['access_token'],
            access_token_secret=account['access_token_secret'],
            proxy=account['proxy']
        )
        for author in authors:
            tweet_unique_quote(client, author, hashtag, used_quotes, limit=5)
            time.sleep(delay_between_tweets)  # Wait for 2 minutes between tweets
