#pricematch

Find the best price for your favorite used hardware on eBay, r/HardwareSwap and more!



Instructions on how to get Ebay notifications working:

PLEASE READ THIS DOCUMENT IN ITS ENTIRETY. EVERYTHING MAY LOOK DAUNTING, BUT TRUST ME, FOLLOW INSTRUCTIONS AND USE GOOGLE AND YOU CAN BE UP AND RUNNING IN 10 MINUTES. I hope I have made everything fairly clear, this should not be terribly difficult to set up if you already have python installed on your machine.

Go to github, use the download link.
Unzip the contents of the github download, save all contents to the same folder. (there are extra files, just ignore them, the important ones are sendemail.py, ebay_scraper.py, ebay_url.py, and listing.py)

You’ll need to be using some sort of python 3 for this, you’ll probably see ‘3.x.x ‘or ‘3.x’ somewhere. I’m sure you know what this is if you’ve installed python before.

Google on how to install each of python modules l’m talking about.
Modules you’ll need: 

-BeautifulSoup

-requests

-lxml

(probably gonna make you use the command line in your computer and type ‘pip install requests’ for example. This may be wrong. Follow the instructions.)

Everything *should* be set up properly.
The code *should* now work. 


Open ebay_scraper.py. 

Scoll to the bottom, under the while(True).


IMPORTANT: Everything you’ll need to change is under the parentheses of notify_me. Here are details about what you’ll need to change. IF SOMETHING IS IN QUOTES, INPUT WHAT YOU NEED INSIDE THE QUOTES. EVERYTHING EXCEPT recipient IS ALREADY PRECONFIGURED, but obviously for my own example searches. Here is what you can change.

-recipient: the email address you want to receive notifications to.

-search_term: what you want to search on ebay.

-maxprice: the highest price you want to search for. Includes item price and shipping, but not tax. Do not put a dollar sign. Use 2 decimal places.

-sortlistings: what order you want your ebay results to show up in, aka “sort by”. You may input ‘newest’ for most recent listings, ‘best’ for most relevant listings, ‘soonest’ for ending soonest, and ‘lowest’ for lowest price. The entire program only works as intended if you use ‘newest’, which is already pre-configured.

-itemcondition: what condition you want to search for. Options: ‘parts’, ‘used’, ‘new’.

-buyitnow: Preconfigured to True. If you want auctions, turn this to False. Otherwise for buy-it-now listings, leave it as-is.

-load_results: how many results to search through every time the program loops. We recommend keeping it at 5 or 10 for highest speed. Of course, if something new comes in it will be the first result, so setting it to 1 or 2 might work fine as well although this has not been tested.


IF YOU’D LIKE TO CHANGE HOW OFTEN THE PROGRAM LOOPS, CHANGE THE NUMBER INSIDE time.sleep(). By default it is 60 for 60 seconds. You can set this to however many seconds you like.

IF YOU WANT MULTIPLE DIFFERENT SEARCHES, simply copy and paste notify_me(everything in here) immediately below the first search, but above time.sleep(x). Change the search term, recipient, maxprice, whatever you like because this is a completely different search.

THAT IS ALL! Run the program and it should loop indefinitely, checking every 60 seconds or whatever you set it to for your personal ebay tastes. It will write to a file, called your_email.dat . This is your profile, and the program will check this file to make sure it does not send duplicate emails. 



