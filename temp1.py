import webscraper
import re
import pandas as pd 
from bs4 import BeautifulSoup

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

soup = webscraper.scrape_page('https://www.reddit.com/r/hardwareswap/comments/k2uhr6/usain_h_huge_lot_of_250_case_fans_led_rgb/')

table = soup.find_all('table')
df = pd.read_html(str(table))[0]

price_re = re.compile(
                r'(bought for |sold for |asking( for)? |selling for |shipped |for |\$(\s)?)?\d{1,4}(\.\d{0,2})?\$?( \$| shipped| local| plus|(\s)?\+|(\s)?obo| or| sold| for|(\s)?USD)*',
                re.IGNORECASE)


for column in range(5): #Find what column prices are in. i is the column's index. Suppose no tables have more than 6.
    try:
        prices = price_re.finditer(df.iloc[0, column])
    except:
        break
    try:
        for price in prices:
            price_string = price.group(0)
            identified_price = identifyprice(price_string)
            if identified_price != None:
                print(identified_price)
                pricecolumnindex = column
                break
    except:  # no prices found, useless af. Raise an error so we will jump to the except: as if no tables found.
        raise NameError('No prices found')

for row in range(len(df.index)):
    item_price = df.iloc[row, pricecolumnindex]
    print(item_price)
