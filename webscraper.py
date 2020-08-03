#scrapes webpage and dumps raw HTML data
import requests
import lxml.html
from bs4 import BeautifulSoup

def scrape_page(page):
    source = requests.get(f'{page}').text
    soup = BeautifulSoup(source, 'lxml')
    return(soup.prettify())



    
    
 
