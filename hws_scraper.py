import praw

#I HAVE CREATED A NEW REDDIT ACCOUNT. USERNAME = 'pcbeest', PASSWORD = 'whataPassword'.

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

subreddit = reddit.subreddit('hardwareswap')

for submission in subreddit.new(limit=10):
    print(submission.title)  # Output: the submission's title
    print(submission.url)    # Output: the submission's URL
    print(submission.link_flair_text)
    print(submission.selftext)
