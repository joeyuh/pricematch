import re
import requests
import lxml.html
from bs4 import BeautifulSoup
import listing
import sendemail

html_template = \
    '''
<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>
<h1 style="text-align: center;"><strong>{0}</strong></h1>
<pre>URL {1}</pre>
<pre>Condition: {2}</pre>
<pre>Price: {3}</pre>
<pre>Shipping: {4}</pre>
<pre>Auction: {5}</pre>
<pre>Best Offer: {6}</pre>
<pre>Images:</pre>
{7}
</body>
</html>
    '''
img_template = '<p><img src="{0}" alt="" /></p>\n'

s = requests.Session()
# searches broken z270 motherboards on ebay
source = s.get(
    'https://www.ebay.com/sch/i.html?_from=R40&_nkw=z270&_sacat=0&LH_TitleDesc=0&LH_ItemCondition=7000&_sop=1&LH_PrefLoc=1').text
soup = BeautifulSoup(source, 'lxml')
html_str = soup.prettify()

# Using regex to search for links to listings, titles, and item condition in the HTML.
# Split method and stuff is used to separate link, titles, and item condition from other useless things.
pattern = re.compile(
    r'href=".+">\n\s+<h3\sclass="s-item__title">\s+.+\n\s+</h3>\n\s*.*\n\s*.*\n\s*.*SECONDARY_INFO">\n\s+.+\n')
listing_results = pattern.findall(html_str)

listings_found = 1
for match in listing_results:
    matched_parts = match.split('\n')
    url = matched_parts[0][6:-2]
    ##print(url)
    listing_title = matched_parts[2][13:]
    ##print(listing_title)
    item_condition = matched_parts[7][13:]
    ##print(item_condition)

    # GOING INTO THE PAGE FOR EACH LISTING, AWAY FROM SEARCH RESULTS PAGE
    r = s.get(str(url))
    page_html = r.text

    # FOR TESTING PURPOSES ONLY
    with open('temp1.html', 'a') as f:
        f.write(page_html)

    # find price on page
    pattern = re.compile(r'>US\s\$\d+\.\d\d')
    matches = pattern.findall(page_html)
    for match in matches:
        item_price = match[4:]
        # print(item_price)

    # Best Offer?
    best_offer = False
    if "Best Offer" in page_html:
        # print('or Best Offer')
        best_offer = True

    # Auction?
    auction_ = False
    if "Current bid" in page_html:
        auction_ = True
    elif "Place bid" in page_html:
        auction_ = True

    # Free Shipping? If no, how much?
    pattern = re.compile(r'fshippingCost.+\n\s+<span>(FREE|\$\d+\.\d+)')
    matches = pattern.findall(page_html)
    # the findall will only find things in the group, so it will only return FREE or $xx.xx.
    for match in matches:
        if match == 'FREE':
            shipping_cost = r'$0.00'
        else:
            shipping_cost = match

    # Description. Description on ebay listings is another webpage. First we find the link to this webpage:
    pattern = re.compile(r'src=".+"\stitle="S')
    matches = pattern.findall(page_html)
    for match in matches:
        # separate the URL from other useless things in the search result
        match = match.split('" ')
        desc_url = match[0][5:]
        # going to the desc_url and getting the HTML data for the page
        r = s.get(desc_url)
        desc_html = r.text
        # searching for the actual description inside the desc_html. This only works when the description is completely unformatted, so doesn't work often.
        pattern = re.compile(r'ds_div">\n\s+(.+)\s</div>')
        matches = pattern.findall(desc_html)
        for match in matches:
            ##print(match)
            pass

    # Find image URLs.
    # Create a set with URLs.
    # Find the first big image.
    image_str = ""
    pattern = re.compile(r'image"\ssrc="(.+)"\ss')
    matches = pattern.findall(page_html)
    for match in matches[:-1]:
        match = match.replace('300', '1000')
        big_image = match
        # print(big_image)
        image_str += img_template.format(big_image)
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
            image_str += img_template.format(full_size_thumbnail_url)

    # create instance of class Listing, starting with name listing1 for instance and so forth, and print attributes of instance
    instance_title = 'listing' + str(listings_found)
    instance_title = listing.Listing(listing_title, url, item_condition, item_price, shipping_cost, best_offer,
                                     auction_)
    print(instance_title.__dict__)



    html=html_template.format(instance_title.Title, instance_title.URL,
                                                                              instance_title.Condition,
                                                                              instance_title.Price,
                                                                              instance_title.Shipping,
                                                                              instance_title.Auction,
                                                                              instance_title.Best_Offer,image_str)
    print(html)
    print(image_str)

    #send an email if price+shipping less than $30 and is not an auction.
    if float(str(instance_title.Price[1:]))+float(str(instance_title.Shipping[1:]))<=30.00 and str(instance_title.Auction) == "False":  
        sendemail.send_an_email(subject=f'We found a {instance_title.Title}', recipient='xxxx@gmail.com',
                                text_content=f'''
Link: {instance_title.URL}

Condition: {instance_title.Condition}
Price: {instance_title.Price}
Shipping: {instance_title.Shipping}
Auction: {instance_title.Auction}
Best Offer: {instance_title.Best_Offer}''', 
        html_content=html)

        print('Sent an email')

    print('\n')