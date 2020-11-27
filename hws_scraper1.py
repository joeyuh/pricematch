import praw
import re
import requests
import time
import pytablereader as ptr
import pytablewriter as ptw
import pandas
import datetime

# homemade modules below!
import sendemail
import webscraper


class HWSPost:
    def __init__(self, title=None, url=None, body=None, timestamp=None, price=''):
        self.title = title
        self.url = url
        self.body = body
        self.timestamp = timestamp
        self.price = price

def animation():
    dot = "."
    i = 0
    while i <= 10:
        print("finding new deals"+i*dot)
        time.sleep(.05)
        i += 1
        print(
            "\033[A                             \033[A")

def uniquify(list1):
    res = []
    for i in list1:
        if i not in res:
            res.append(i)
    return res


# I HAVE CREATED A NEW REDDIT ACCOUNT. USERNAME = 'pcbeest', PASSWORD = 'whataPassword'.


client_id = 'oA7oqPSjXGLeAw'
client_secret = 'rxQEH9FajvtDvr-PoxtjmEvxEKw'
user_agent = "hws_scrape"
username = 'pcbeest'
password = 'whataPassword'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

list_of_posts = []  # Created so that we can display only new and unseen posts
res = []
while True:
    subreddit = reddit.subreddit('hardwareswap')

    for submission in subreddit.new(limit=10): #REFRESH AND LOOK FOR NEW POSTS AND PROCESS THEM
        try:
            global want
            want = submission.title.split('[W]')[1]
        except:
            continue
        if 'paypal' in want.lower(): #aka if it's a selling post
            #CREATE INSTANCE OF CLASS HWSPOST, GIVE IT ATTRIBUTES OF TITLE, BODY, URL.
            post_items = submission.title.split('[H]')[1].split('[W]')[0]
            post_body = submission.selftext
            post_url = submission.url.strip()
            #print(post_items) #Print what they're selling
            #print(post_body+3*'\n')

            post_items = HWSPost(title=post_items, body=post_body, url=post_url)
            list_of_posts.append(post_items)

            #SEE IF POST HAS ALREADY BEEN PROCESSED
            res_length_before = len(res)
            for element in list_of_posts:
                inres = False
                if len(res) == 0:
                    res.append(element)
                elif len(res) != 0:
                    for item in res:
                        if element.title == item.title:
                            inres = True
                    if inres == False:
                        res.append(element)
            res_length_after = len(res)
            #SKIP PROCESSING OF POSTS THAT HAVE ALREADY BEEN PROCESSED
            if res_length_after - res_length_before == 0:
                animation()
                continue

            #FIND PRICES in post_body
            price_re = re.compile(
            r'(bought for\s|sold for\s|asking( for)?\s|selling for\s)?\$?\d{1,4}(\.\d{0,2})?\$?\s?(shipped|local|plus|\+|obo|or|sold|for)*',
            re.IGNORECASE)
            prices = price_re.finditer(post_body)
            for price in prices:
                price_string = price.group(0)
                if 'bought' in price_string or 'sold' in price_string:  #Already sold or he bought for $x, not relevant to us.
                    continue
                price_string = price_string.lower().replace(' ', '').replace('sold', '')
                try: # If the string only has numbers, it's an irrelevant random number
                    temp = float(price_string)
                except ValueError: #There are words or a dollar sign, indicating it's not a random model number
                    post_items.price += f'{price_string.strip()}, '


            #FIND TIMESTAMP LINKS IN THE POST'S SOURCE CODE AND ATTRIBUTE THEM TO THE CLASS INSTANCE
            source = webscraper.scrape_page(post_url)
            search_string = r'(imgur\.com/(a/)?.+|imgur.com/gallery/.+|ibb.co/.+)'
            timestamp_urls = re.finditer(search_string, source)
            post_items.timestamp = []
            for match in timestamp_urls:
                timestamp = str(match).split("match='")[1].split('"')[0]
                post_items.timestamp.append(timestamp)
                post_items.timestamp = uniquify(post_items.timestamp)

            if res_length_after - res_length_before != 0:
                difference = res_length_after - res_length_before
                for element in res[-1*difference:]:
                    print(element.title+" - "+element.url)
                    print(element.price+'\n')

    time.sleep(1)    

