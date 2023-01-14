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


class HWSPost:
    def __init__(self, title, url, body, timestamp, price):
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

# I HAVE CREATED A NEW REDDIT ACCOUNT. USERNAME = 'pcbeest', PASSWORD = 'whataPassword'.


client_id = 'client_id'
client_secret = 'client_secret'
user_agent = "user_agent"
username = 'username'
password = 'password'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

list_of_posts = []  # Created so that we can display only new and unseen posts

while True:
    subreddit = reddit.subreddit('hardwareswap')
    for submission in subreddit.new(limit=4):
        try:
            listing_text = submission.selftext
            # print(submission.link_flair_text)

            title = submission.title.split("[H]")
            title = title[1].split("[W]")

            if "paypal" in title[1].lower():
                if len(list_of_posts) == 0 or title[0] != list_of_posts[-1].title or title[0] != list_of_posts[-2].title or title[0] != list_of_posts[-3].title or title[0] != list_of_posts[-4].title:
                    # We have now seen this post once, writing to list
                    print(len(list_of_posts))
                    listing_title = title[0]
                    instance = title[0]
                    instance = HWSPost

                    instance.title = listing_title
                    instance.url = submission.url.strip()
                    instance.body = submission.selftext
                    instance.price = ''
                    list_of_posts.append(instance)
                    print(list_of_posts[-1].title)

                    #print(instance.title)
                    #print(instance.url)
                    #print(instance.body) #THIS IS THE TEXT OF THE POST!
                    #print(instance.price)
                    if '|' in instance.body:
                        print('Table:')
                        #print(listing_text)
                        loader = ptr.MarkdownTableTextLoader(
                            text=submission.selftext)
                        writer = ptw.TableWriterFactory.create_from_format_name(
                            "rst")
 
                        for table_data in loader.load():
                             writer.from_tabledata(table_data)
                             writer.write_table()
                        # print(table_data.as_dataframe())
                    else:
                        final_item_count = 0
                        item_count = 0    # How many item do we think there is in the listing
                        price_count = 0   # How many prices we think there is in the listing
                        splitter_found = False
                        if ',' in instance.title:
                            splitter_found = True
                            items = instance.title.split(',')
                            for item in items:
                                redacted = item.lower().replace(' ', '').replace('bnib', '').replace('new', '')\
                                    .replace('unopened', '').replace('used', '')
                                if redacted == '':
                                    items.remove(item)
                            item_count = len(items)
                        elif '|' in instance.title:   # Yes, someone used this to split the item
                            splitter_found = True
                            items = instance.body.split('|')
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
                                pass
                                instance.price += '\n'+price_string
                                #print(instance.price)


                        # find imgur link url. People might timestamp in other sites, but ....
                        imgur_url = re.compile(
                            r'(imgur\.com/a/.+|imgur.com/gallery/.+|ibb.co/.+)')
                        imgur_urls = imgur_url.finditer(listing_text)
                        try:
                            for url in imgur_urls:
                                instance.timestamp = instance.timestamp + url.group(0)
                            #print(instance.timestamp)
                        except:
                            instance.timestamp = 'no timestamps'


                        # delete all other URLs
                        findurls = re.compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}\
                            |www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|\
                            https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
                        deletedurls = findurls.finditer(listing_text)
                        try:
                            for link in deletedurls:
                                listing_text.replace(f'{link}', '')
                                #print(f"Deleted url:{link}")
                        except:
                            pass


                        print(instance.title)
                        print(instance.url.strip())
                        print(instance.price.strip())
                        #print(instance.timestamp)

                        currenttime = str(datetime.datetime.now())
                        print("found at " + currenttime[11:-7])   

                        print('\n')
                else:
                    animation()
            else:
                animation()
        except:
            animation()
            pass
    time.sleep(1)

    # housekeeping to make sure the list doesn't get too long and destroy RAM:
    if len(list_of_posts) >= 20:
        list_of_posts.pop(0)
