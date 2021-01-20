import datetime
import re
import threading
import time

import beepy
import praw
import pytablereader as ptr
import tkinter as tk
import markdown2
from tkinterhtml import HtmlFrame

AUDIO_ALERT = True


class HWSPost:
    def __init__(self, title=None, url=None, body=None, author=None, timestamps=None, price='', tableexists=None):
        self.title = title
        self.url = url
        self.body = body
        self.author = author
        self.timestamps = timestamps
        self.price = price
        self.tableexists = tableexists
        self.urls = []  # all urls in a most


def alert():
    beepy.beep(sound=4)


def animation():
    dot = "."
    i = 0
    while i <= 10:
        print("finding new deals" + i * dot)
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


def identifyprice(price_string):
    price_string = price_string.lower().strip()
    try:  # If the string only has numbers, it's an irrelevant random number
        price_string = float(price_string)
        return None
    except ValueError:  # There are words or a dollar sign, indicating it's not a random model number
        if 'bought' in price_string or 'sold' in price_string:
            return None
        else:
            return price_string


# I HAVE CREATED A NEW REDDIT ACCOUNT. USERNAME = 'pcbeest', PASSWORD = 'whataPassword'.
reddit = praw.Reddit(client_id='oA7oqPSjXGLeAw',
                     client_secret='rxQEH9FajvtDvr-PoxtjmEvxEKw',
                     user_agent="hws_scrape",
                     username='pcbeest',
                     password='whataPassword')

print('')
list_of_posts = []  # Created so that we can display only new and unseen posts
res = []  # res is the list of unduplicated posts.

root = tk.Tk()
while True:
    subreddit = reddit.subreddit('hardwareswap')
    try:  # Praw might throw errors, we want to ignore them
        for submission in subreddit.stream.submissions():  # REFRESH AND LOOK FOR NEW POSTS AND PROCESS THEM
            try:
                h = submission.title.lower().find('[h]')
                w = submission.title.lower().find('[w]')
                if w > h:
                    want = submission.title.lower().split('[w]')[1]
                else:
                    want = submission.title.lower().split('[h]')[0]
            except:
                continue

            if 'paypal' in want.lower():  # aka if it's a selling post

                html = f'<html><body>{markdown2.markdown(submission.selftext)}</body></html>'
                frame = HtmlFrame(root, horizontal_scrollbar="auto")
                frame.grid(sticky=tk.NSEW)
                frame.set_content(html)
                root.columnconfigure(0, weight=1)
                root.rowconfigure(0, weight=1)
                root.update_idletasks()
                root.update()

                # CREATE INSTANCE OF CLASS HWSPOST, GIVE IT ATTRIBUTES OF TITLE, BODY, URL.
                try:
                    post_title = submission.title.split('[H]')[1].split('[W]')[0]
                    post_body = submission.selftext.replace(',', '')  # Remove ',' in price tags
                    post_url = submission.url.strip()
                    post_author = submission.author

                    post = HWSPost(title=post_title, body=post_body, author=post_author, url=post_url)
                    list_of_posts.append(post)
                except:
                    continue

                # SEE IF POST HAS ALREADY BEEN PROCESSED
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
                # SKIP PROCESSING OF POSTS THAT HAVE ALREADY BEEN PROCESSED
                if res_length_after - res_length_before == 0:
                    # animation()
                    continue

                search_string = r'(http(s)?://)?(i.)?(imgur.com/gallery/[\w\d]{5,8}|imgur\.com/(a/)?[\w\d]{5,7}|ibb.co/.{5,7})'
                timestamp_urls = re.finditer(search_string, str(post.body))
                post.timestamps = []
                for match in timestamp_urls:
                    timestamp = match.group(0)
                    post.timestamps.append(timestamp)
                    post.timestamps = uniquify(post.timestamps)

                    all_urls = re.finditer(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,'
                                           r'}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|('
                                           r'?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', str(post.body))

                    for match in all_urls:
                        url = str(match.group(0)).replace('(', '').replace(')', '')
                        post.body = post.body.replace(url, '')  # remove all url for better price matching
                        if len(post.timestamps) == 0:  # If we dont have any imgur or ibb link
                            post.urls.append(url)  # append all links in the most

                # FIND PRICES.
                price_re = re.compile(
                    r'(bought for |sold for |asking( for)? |selling for |shipped |for |\$(\s)?)?(?<!\dx)' #search for keywords, but not nxn (RAM)
                    r'\d{1,4}(\.\d{0,2})?\$?' #search for numbers and decimal places, and dollar sign after the number.
                    r'(?!\+ bronze|\+ gold|\+ silver|\+ certified|\+ platinum)' #don't match 80+ ratings.
                    r'( \$| shipped| local| plus|(\s)?\+|(\s)?obo| or| sold| for|(\s)?USD)*', #match these keywords
                    re.IGNORECASE)

                if '|' in post.body:  # | means we found a table
                    loader = ptr.MarkdownTableTextLoader(text=post.body)
                    dfs = []
                    for table_data in loader.load():
                        df = table_data.as_dataframe()
                        dfs.append(df)

                        for column in range(len(df.columns)):  # Find what column prices are in.
                            prices = price_re.finditer(str(df.iloc[0, column]))
                            try:
                                for price in prices:
                                    price_string = price.group(0)
                                    identified_price = identifyprice(price_string)
                                    if identified_price != None:
                                        pricecolumnindex = column
                                        post.tableexists = True
                                        break
                            except:
                                # no prices found, useless af. Raise an error so we will jump to the except:
                                # as if no tables found.
                                print('No prices found in table')

                if not post.tableexists:  # no useful tables found
                    prices = price_re.finditer(post.body)
                    for price in prices:
                        price_string = price.group(0)
                        identified_price = identifyprice(price_string)
                        if identified_price != None:
                            post.price += f'{identified_price};  '

                # IF NEW POSTS HAVE BEEN FOUND, PRINT THEM OUT
                if res_length_after - res_length_before > 0:
                    if AUDIO_ALERT:
                        alert_thread = threading.Thread(target=alert)
                        alert_thread.start()  # Start audio thread to play in background
                        # no need to join, it will finish itself
                    difference = res_length_after - res_length_before
                    for element in res[-1 * difference:]:
                        print(element.title + " - " + element.url)
                        if not element.tableexists:
                            if element.price == '':
                                print('Unable to find price')
                            else:
                                print(element.price[:-2])
                        else:
                            print('TABLE FOUND:')
                            for df in dfs:
                                for row in range(len(df.index)):
                                    item = df.iloc[row, 0]
                                    item_price = df.iloc[row, pricecolumnindex]
                                    print(f'{item} - {item_price}')
                        try:
                            if len(element.timestamps) == 0:
                                print('Could not find any timestamps on imgur or ibb.co, here is all urls in the '
                                      'listing:')
                                print(element.urls)
                            elif len(element.timestamps) == 1:
                                print(str(element.timestamps[0]))
                            else:
                                print(element.timestamps)
                        except:
                            pass
                        currenttime = str(datetime.datetime.now())
                        print(f'Send A PM:  https://www.reddit.com/message/compose/?to={element.author}')
                        print("found at " + currenttime[11:-7])
                        print('')
    except Exception as e:
        print(f'Reddit Error: {e}\n Continuing')

    time.sleep(1)
