import praw
import re
import requests
#homemade modules below!
import sendemail

#I HAVE CREATED A NEW REDDIT ACCOUNT. USERNAME = 'pcbeest', PASSWORD = 'whataPassword'.

client_id = 'oA7oqPSjXGLeAw'
client_secret = 'rxQEH9FajvtDvr-PoxtjmEvxEKw'
user_agent = "hws_scrape"
username = 'pcbeest'
password = 'whataPassword'

reddit = praw.Reddit(client_id = client_id, 
                    client_secret = client_secret,
                    user_agent = user_agent,
                    username = username,
                    password = password)

subreddit = reddit.subreddit('hardwareswap')

s = requests.Session()
useragent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
for submission in subreddit.new(limit=10):
    listing_data = submission.selftext

    if submission.link_flair_text == 'SELLING':
        print(submission.url)
        print(submission.link_flair_text)
        print(submission.title)
        print(submission.selftext)

        #find imgur link url. People might timestamp in other sites, but ....
        pattern = re.compile(r'https://imgur\.com/a/.......')
        matches = pattern.findall(listing_data)
        for match in matches: 
            print(match)


        print('\n\n\n')
            
