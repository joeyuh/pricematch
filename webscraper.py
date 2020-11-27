#scrapes webpage and dumps raw HTML data
import requests
import lxml.html
from bs4 import BeautifulSoup

def scrape_page(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    source = requests.get(f'{page}', headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    return(soup.prettify())



    
    
 
