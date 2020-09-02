import praw

client_id = 'oA7oqPSjXGLeAw'
client_secret = 'rxQEH9FajvtDvr-PoxtjmEvxEKw'
user_agent = "hws_scrape"
username = 'pcbeest'
password = 'whataPassword'

reddit = praw.Reddit(client_id = client_id, 
                    client_secret = client_secret,
                    user_agent = user_agent,
                    username = username,
                    password = password)

subred = reddit.subreddit('hardwareswap')

hws_new = subred.new(limit=10)

x = next(hws_new)

for i in hws_new:
    print(i.title)
