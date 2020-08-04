import requests
import re
import listing
import pickle
import os
import ebay_url

listing_set = set()
search_terms = ['lga 1151 motherboard', 'lga 1150 motherboard', 'lga 1155 motherboard', 'z68 motherboard',
                'z77 motherboard', 'z87 motherboard', 'z97 motherboard', 'z170 motherboard', 'z270 motherboard',
                'z370 motherboard', 'z390 motherboard', 'z490 motherboard']

# Not in use currently, reserved
def load():
    if os.path.exists(r'.\MassDL\set.dat'):
        with open(r'.\MassDL\set.dat', 'rb') as set_file:
            listing_set = pickle.load(set_file)
            print(f'Loaded {len(listing_set)} from saved file')
    else:
        print('File not found, proceeding with empty set.')


# Copied from ebay_scrap.py CURRENTLY PRINTING URL ONLY
def download(s: requests.Session,url):
    s = requests.Session()
    page_html = s.get(url).text
    pattern = re.compile(r'image"\ssrc="(.+)"\ss')
    matches = pattern.findall(page_html)
    for match in matches[:-1]:
        match = match.replace('300', '1000')
        print(match)
        big_image = match
    # Find the small images (thumbanails).
    pattern = re.compile(r'img\ssrc="(.+)"\sstyle')
    matches = pattern.findall(page_html)
    for match in matches:
        full_size_thumbnail_url = match.replace('64', '1000')
        # making sure we don't get the big image and the same thumbnail
        if big_image == full_size_thumbnail_url:
            pass
        else:
            print(full_size_thumbnail_url)


if __name__ == "__main__":
    s = requests.Session()
    for term in search_terms:
        res = ebay_url.get_listing_urls(s,term)
        for url in res:
            download(s,url)
