import requests
import os
import pickle
import re
from multiprocessing import Pool

s = requests.Session()
listing_set = set()
listing_list = list()


def download(url):
    global s
    get = requests.get(url, stream=True)
    if get.status_code == 200:
        file_name = re.match(r'.*/.*/(.*)/.*', url).group(1)
        with open(f'{file_name}.jpg', 'wb') as img:
            for chunk in get.iter_content(chunk_size=1024):
                img.write(chunk)
    else:
        print(f'Error Code {get.status_code}')


def load():
    global listing_set
    if os.path.exists(r'set.dat'):
        with open(r'set.dat', 'rb') as set_file:
            listing_set = pickle.load(set_file)
            print(f'Loaded {len(listing_set)} from saved file')
    else:
        print('File not found, proceeding with empty set.')


if __name__ == '__main__':
    load()
    listing_list = list(listing_set)
    p = Pool()
    p.map(download, listing_list)
    p.close()
    p.join()