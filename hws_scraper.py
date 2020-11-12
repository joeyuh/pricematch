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


class HWSItem:
    def __init__(self):
        self.price_str = ''
        self.price = 0
        self.name = ''


def animation():
    dot = "."
    i = 0
    while i <= 10:
        print("finding new deals"+i*dot)
        time.sleep(.05)
        i += 1
        print(
            "\033[A                             \033[A")

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

s = requests.Session()
useragent = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}

list_of_posts = []  # Created so that we can display only new and unseen posts

while True:
    subreddit = reddit.subreddit('hardwareswap')
    for submission in subreddit.new(limit=5):
        try:
            listing_text = submission.selftext
            # print(submission.link_flair_text)
            title = submission.title.split("[H]")
            title = title[1].split("[W]")

            if "paypal" in title[1].lower():
                if title[0] not in list_of_posts:
                    # We have now seen this post once, writing to list
                    list_of_posts.append(title[0])
                    # print(list_of_posts)
                    print(title[0])
                    print(submission.url)
                    # print(submission.selftext) #THIS IS THE TEXT OF THE POST!
                    if '|' in submission.selftext:
                        print('Table:')
                        #print(listing_text)
                        loader = ptr.MarkdownTableTextLoader(text=submission.selftext)
                        writer = ptw.TableWriterFactory.create_from_format_name("rst")
 
                        for table_data in loader.load():
                            writer.from_tabledata(table_data)
                            writer.write_table()
                        #print(table_data.as_dataframe())
                    else:
                        final_item_count = 0
                        item_count = 0    # How many item do we think there is in the listing
                        price_count = 0   # How many prices we think there is in the listing
                        splitter_found = False
                        if ',' in title[0]:
                            splitter_found = True
                            items = title[0].split(',')
                            for item in items:
                                redacted = item.lower().replace(' ', '').replace('bnib', '').replace('new', '')\
                                    .replace('unopened', '').replace('used', '')
                                if redacted == '':
                                    items.remove(item)
                            item_count = len(items)
                        elif '|' in title[0]:   # Yes, someone used this to split the item
                            splitter_found = True
                            items = title[0].split('|')
                            # print(items)
                        else:
                            item_count = 1
                            #print(f'Item count {item_count}')
                            # find the price of the item
                            price_re = re.compile(
                                r'(bought for\s|sold for\s|asking( for)?\s|selling for\s)?\$?\d{1,4}(\.\d{0,2})?\$?\s?(shipped|local|plus|\+|obo|or|sold)*',
                                re.IGNORECASE)

                        prices = price_re.finditer(listing_text)
                        for price in prices:
                            # print(price.groups())
                            price_string = price.group(0)
                            if 'bought' in price_string or 'sold' in price_string:  # No sold or brought info
                                print(f'Deleted {price_string}')
                                continue
                            price_string = price_string.lower().replace('.', '') \
                                .replace(' ', '').replace('sold', '')

                            try:
                                # If the string only have number left (no asking, $ or shipped)
                                # It is not a price
                                temp = float(price_string)
                                #print(f'Deleted {temp}')
                            except ValueError:   # Otherwise we are fine
                                print(price_string)
                                pass

                        # find imgur link url. People might timestamp in other sites, but ....
                        imgur_url = re.compile(
                            r'(imgur\.com/a/.+|imgur.com/gallery/.+|ibb.co/.+)')
                        imgur_urls = imgur_url.finditer(listing_text)
                        for url in imgur_urls:
                            pass
                            print(url.group(0))

                        # delete all other URLs
                        findurls = re.compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}\
                            |www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|\
                            https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
                        deletedurls = findurls.finditer(listing_text)
                        for link in deletedurls:
                            listing_text.replace(f'{link}', '')
                            #print(f"Deleted url:{link}")

                        currenttime = str(datetime.datetime.now())
                        print("found at " + currenttime[11:-7])   

                        print('\n')
                        animation()
                else:
                    animation()
        except:
            pass
    time.sleep(1)

    # housekeeping to make sure the list doesn't get too long and destroy RAM:
    if len(list_of_posts) >= 20:
        list_of_posts.pop(0)
