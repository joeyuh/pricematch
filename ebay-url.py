import requests

def get_listing_urls(searchterm):
    s = requests.Session()
    html_data = s.get(f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR12.TRC2.A0.H0.X{searchterm}.TRS0&_nkw={searchterm}&_sacat=0').text
    return(html_data)

print(get_listing_urls('i7'))