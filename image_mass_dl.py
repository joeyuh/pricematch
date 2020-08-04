import requests
import re
import listing
import pickle
import os
import ebay_url
import sys

total_fetched = 0
listing_set = set()
search_terms = ['lga 1151 motherboard', 'lga 1150 motherboard', 'lga 1155 motherboard', 'lga1156 motherboard',
                'z68 motherboard', 'z75 motherboard', 'z77 motherboard', 'z87 motherboard', 'z97 motherboard',
                'z170 motherboard', 'z270 motherboard',
                'z370 motherboard', 'z390 motherboard', 'z490 motherboard', 'h55 motherboard', 'h61 motherboard',
                'h67 motherboard', 'h77 motherboard' 'h81 motherboard', 'h87 motherboard',
                'h97 motherboard', 'h110 motherboard', 'h170 motherboard', 'h310 motherboard', 'h270 motherboard',
                'h370 motherboard', 'h410 motherboard',
                'b360 motherboard', 'b150 motherboard', 'b250 motherboard', 'b365 motherboard', 'b460 motherboard',
                'b85 motherboard', 'b75 motherboard', 'h67 motherboard', 'p67 motherboard']


def load():
    global listing_set
    if os.path.exists(r'set.dat'):
        with open(r'set.dat', 'rb') as set_file:
            listing_set = pickle.load(set_file)
            print(f'Loaded {len(listing_set)} from saved file')
    else:
        print('File not found, proceeding with empty set.')


def save():
    global listing_set
    with open(r'set.dat', 'wb') as set_file:
        pickle.dump(listing_set, set_file)


# Copied from ebay_scrap.py CURRENTLY PRINTING URL ONLY
def download(s: requests.Session, url):
    global total_fetched
    global listing_set
    s = requests.Session()
    page_html = s.get(url).text
    pattern = re.compile(r'image"\ssrc="(.+)"\ss')
    matches = pattern.findall(page_html)
    for match in matches[:-1]:
        match = match.replace('300', '1000')
        # print(match)
        listing_set.add(match)
        big_image = match
        total_fetched += 1
        sys.stdout.write("\rFetched %i" % total_fetched)
        sys.stdout.flush()
    # Find the small images (thumbanails).
    pattern = re.compile(r'img\ssrc="(.+)"\sstyle')
    matches = pattern.findall(page_html)
    for match in matches:
        full_size_thumbnail_url = match.replace('64', '1000')
        # making sure we don't get the big image and the same thumbnail
        if big_image == full_size_thumbnail_url:
            pass
        else:
            # print(full_size_thumbnail_url)
            listing_set.add(full_size_thumbnail_url)
            total_fetched += 1
            sys.stdout.write("\rFetched %i" % total_fetched)


if __name__ == "__main__":
    s = requests.Session()
    load()
    for term in search_terms:
        res = ebay_url.get_listing_urls(s, term, item_condition="parts")
        for url in res:
            download(s, url)
            save()
