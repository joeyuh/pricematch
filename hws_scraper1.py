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
    def __init__(self, title=None, url=None, body=None, timestamp=None, price='', tableexists=None):
        self.title = title
        self.url = url
        self.body = body
        self.timestamp = timestamp
        self.price = price
        self.tableexists = tableexists

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
res = [] #res is the list of unduplicated posts.
while True:
    subreddit = reddit.subreddit('hardwareswap')

    for submission in subreddit.new(limit=100): #REFRESH AND LOOK FOR NEW POSTS AND PROCESS THEM
        try:
            global want
            want = submission.title.split('[W]')[1]
        except:
            continue

        if 'paypal' in want.lower(): #aka if it's a selling post

            #CREATE INSTANCE OF CLASS HWSPOST, GIVE IT ATTRIBUTES OF TITLE, BODY, URL.
            try:
                post_items = submission.title.split('[H]')[1].split('[W]')[0]
                post_body = submission.selftext
                post_url = submission.url.strip()

                post_items = HWSPost(title=post_items, body=post_body, url=post_url)
                list_of_posts.append(post_items)
            except:
                continue

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

            #FIND TIMESTAMP LINKS IN THE POST'S SOURCE CODE AND ATTRIBUTE THEM TO THE CLASS INSTANCE
            source = webscraper.scrape_page(post_url)
            search_string = r'href="(http(s)?://)?(i.)?(imgur\.com/(a/)?\w{5,7}|imgur.com/gallery/\w{5,7}|ibb.co/.{5,7})'
            timestamp_urls = re.finditer(search_string, str(source))
            post_items.timestamp = []
            for match in timestamp_urls:
                timestamp = match.group(0)[6:]
                post_items.timestamp.append(timestamp)
                post_items.timestamp = uniquify(post_items.timestamp)

            #FIND PRICES. First, check if there is table, if not, just find prices.
            price_re = re.compile(
                r'(bought for |sold for |asking( for)? |selling for |shipped |for |\$(\s)?)?\d{1,4}(\.\d{0,2})?\$?( \$| shipped| local| plus|(\s)?\+|(\s)?obo| or| sold| for|(\s)?USD)*',
                re.IGNORECASE)
            try: #try and find tables. If table, try to find the prices in the table. Otherwise, just pass.
                post_items.tableexists = False
                table = source.find_all('table') #source code was found before when we found image links
                df = pandas.read_html(str(table))[0]
                for column in range(5): #Find what column prices are in. i is the column's index. Suppose no tables have more than 6.
                    try: #Don't know how many columns there are! So we have to try.
                        prices = price_re.finditer(df.iloc[0, column])
                    except:
                        break
                    try:
                        for price in prices:
                            price_string = price.group(0)
                            identified_price = identifyprice(price_string)
                            if identified_price != None:
                                pricecolumnindex = column
                                post_items.tableexists = True
                                break
                    except:  # no prices found, useless af. Raise an error so we will jump to the except: as if no tables found.
                        raise NameError('No prices found')
            except: #no useful tables found
                prices = price_re.finditer(post_body)
                for price in prices:
                    price_string = price.group(0)
                    identified_price = identifyprice(price_string)
                    if identified_price != None:
                        post_items.price += f'{identified_price}, '


            #IF NEW POSTS HAVE BEEN FOUND, PRINT THEM OUT
            if res_length_after - res_length_before > 0:
                difference = res_length_after - res_length_before
                for element in res[-1*difference:]:
                    print(element.title+" - "+element.url)
                    if element.tableexists == False:
                        if element.price == '':
                            print('Unable to find price')
                        else:
                            print(element.price)
                    elif element.tableexists == True:
                        print('TABLE FOUND:')
                        for row in range(len(df.index)):
                            item = df.iloc[row, 0]
                            item_price = df.iloc[row, pricecolumnindex]
                            print(f'{item} - {item_price}')
                    try:
                        if len(element.timestamp) == 0:
                            print('Could not find any timestamps on imgur/ibb.co')
                        elif len(element.timestamp) == 1:
                            print(str(element.timestamp[0]))
                        else:
                            print(element.timestamp)
                    except:
                        pass
                    currenttime = str(datetime.datetime.now())
                    print("found at " + currenttime[11:-7])
                    print('')

    time.sleep(0)    

