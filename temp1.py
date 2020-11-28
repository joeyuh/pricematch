import webscraper
import re

source = webscraper.scrape_page('https://www.reddit.com/r/hardwareswap/comments/k2bm3j/usaor_h_xbox_one_x_note_20_ultra_crossfade_codec/')

with open('temp1.txt', 'r') as f:
    search_string = r'href="(https://)?(imgur\.com/(a/)?.+|imgur.com/gallery/.+|ibb.co/.+)"'
    timestamp_urls = re.finditer(search_string, source)
    for match in timestamp_urls:
        if '"' not in str(match.group()):
            print(match.group())