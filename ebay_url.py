import requests
import re
from bs4 import BeautifulSoup


def get_listing_urls(searchterm):
    splitted_searchterm = searchterm.split(' ')

    urls = []
    html_data = ""
    s = requests.Session()
    final_search_query = ""
    if len(splitted_searchterm) == 1:
        query_url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR12.TRC2.A0.H0.X{splitted_searchterm[0]}.TRS0&_nkw={splitted_searchterm[0]}&_sacat=0&_ipg=200&_pgn='
        final_search_query = query_url
    elif len(splitted_searchterm) > 1:
        query_url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR12.TRC2.A0.H0.X.TRS0&_nkw=&_sacat=0&_ipg=200&_pgn='
        query_url = query_url.split('.TRS')
        x = query_url[1].split('nkw=')
        query_url.pop()
        query_url.append(x[0])
        query_url.append(x[1])

        query_url[0] += '.TRS'
        query_url[1] += 'nkw='
        for i in range(len(splitted_searchterm) - 1):
            query_url[0] += f'{splitted_searchterm[i]}' + '+'
            query_url[1] += f'{splitted_searchterm[i]}' + '+'
        query_url[0] += f'{splitted_searchterm[-1]}'
        query_url[1] += f'{splitted_searchterm[-1]}'

        final_search_query = query_url[0] + query_url[1] + query_url[2]

    i = 1
    while True:
        html_data = s.get(final_search_query + str(i)).text

        source = html_data
        soup = BeautifulSoup(source, 'lxml')
        source = soup.prettify()
        with open("1.txt", "w") as f:
            f.write(source)

        pattern = re.compile(
            r'href=".+">\n\s+<h3\sclass="s-item__title">\s+.+\n\s+</h3>\n\s*.*\n\s*.*\n\s*.*SECONDARY_INFO">\n\s+.+\n')
        listing_results = pattern.findall(source)

        for match in listing_results:
            matched_parts = match.split('\n')
            url = matched_parts[0][6:-2]
            urls.append(url)

        # detect if the next paged button is disabled
        pattern = re.compile(r'<a _sp=".+".*aria-label="Next page"')
        listing_results = pattern.findall(source)
        if 'disabled' in listing_results[0]:
            break
        i += 1
    return urls
