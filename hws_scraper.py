import praw
import re
import requests
import time
import pytablereader as ptr
import pytablewriter as ptw
import pandas

# homemade modules below!
import sendemail

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

while True:
    subreddit = reddit.subreddit('hardwareswap')
    for submission in subreddit.new(limit=200):
        try:
            listing_text = submission.selftext
            # print(submission.link_flair_text)
            submission.title = submission.title.split("[H]")
            submission.title = submission.title[1].split("[W]")

            if "paypal" in submission.title[1].lower():
                print(submission.title[0])
                print(submission.url)
                # print(submission.selftext) #THIS IS THE TEXT OF THE POST!

                if '|' in submission.selftext:  # we found a table
                    print('Table:')
                    # print(listing_text)
                    loader = ptr.MarkdownTableTextLoader(text=submission.selftext)
                    writer = ptw.TableWriterFactory.create_from_format_name("rst")
                    for table_data in loader.load():
                        writer.from_tabledata(table_data)
                        writer.write_table()
                        # print(table_data.as_dataframe())
                else:
                    # find the price of the item
                    price_re = re.compile(
                        r'(bought for|sold for|asking( for)?|selling for)?\s?\$?\d{1,4}(\.\d{0,2})?\$?\s?(shipped|local|plus|\+|obo|or|sold)?',
                        re.IGNORECASE)

                    prices = price_re.finditer(listing_text)
                    for price in prices:
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
                            # print(f'Deleted {temp}')
                        except ValueError:   # Otherwise we are fine
                            print(price_string)

                    # find imgur link url. People might timestamp in other sites, but ....
                    imgur_url = re.compile(r'imgur\.com/a/.......')
                    imgur_urls = imgur_url.finditer(listing_text)
                    for url in imgur_urls:
                        # print(url)
                        pass

                    print('\n')
                # break
        except:
            pass
        # time.sleep(0.5)
    break
