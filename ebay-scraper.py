import webscraper
import re
import requests

class Listing:
    def __init__(self, Title, URL, Condition, Price, Best_Offer=False, Auction=False):
        self.Title = Title
        self.URL = URL
        self.Condition = Condition
        self.Price = Price
        self.Best_Offer = Best_Offer
        self.Auction = Auction

#Uses the webscraper module to get the HTML data for the eBay search page, in this case for broken Z170 motherboards
html_str = webscraper.scrape_page('https://www.ebay.com/sch/i.html?_from=R40&_nkw=z170&_sacat=0&LH_TitleDesc=0&LH_ItemCondition=7000&_sop=1')


#Using regex to search for links to listings, titles, and item condition in the HTML. 
#Split method and stuff is used to separate link, titles, and item condition from other useless things.
pattern = re.compile(r'href=".+">\n\s+<h3\sclass="s-item__title">\s+.+\n\s+</h3>\n\s*.*\n\s*.*\n\s*.*SECONDARY_INFO">\n\s+.+\n')
matches = pattern.findall(html_str)

for match in matches[:3]:
    matched_parts = match.split('\n')
    url = matched_parts[0][6:-2]
    ##print(url)
    listing_title = matched_parts[2][13:]
    ##print(listing_title)
    item_condition = matched_parts[7][13:]
    ##print(item_condition)
    
    #GOING INTO THE PAGE FOR EACH LISTING, AWAY FROM SEARCH RESULTS PAGE
    s = requests.Session()
    r = s.get(str(url))
    page_html = r.text

    #find price on page
    pattern = re.compile(r'>US\s\$\d+\.\d\d')
    matches = pattern.findall(page_html)
    for match in matches:
        item_price = match[4:]
        #print(item_price)

    #Best Offer?
    best_offer = False
    if "Best Offer" in page_html:
        #print('or Best Offer')
        best_offer = True
    
    #Auction?
    auction_ = False
    if "Current bid" in page_html:
        auction_ = True

    #create instance of class Listing, starting with name listing1 for instance and so forth, and print attributes of instance
    instance_title = 'listing' + str(listings_found)
    instance_title = Listing(listing_title, url, item_condition, item_price, best_offer, auction_)
    print(instance_title.__dict__)
    
    print('\n')
