#scrapes webpage and dumps raw HTML data

def scrape_page(page):
    import requests
    import lxml.html
    from bs4 import BeautifulSoup
    source = requests.get(f'{page}').text
    soup = BeautifulSoup(source, 'lxml')
    return(soup.prettify())



    
    
 
