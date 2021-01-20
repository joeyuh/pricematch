import praw
import math
import pandas as pd
from psaw import PushshiftAPI
import datetime

client_id = 'oA7oqPSjXGLeAw'
client_secret = 'rxQEH9FajvtDvr-PoxtjmEvxEKw'
user_agent = "hws_scrape"
username = 'pcbeest'
password = 'whataPassword'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)
api = PushshiftAPI(reddit)

list_of_posts = []  # Created so that we can display only new and unseen posts

subreddit = reddit.subreddit('hardwareswap')
hwsbot_response_time = pd.Series(dtype='float64')
comment_data = pd.DataFrame(
    columns=['latency', 'author', 'comment_created_utc', 'faster_than_hwsbot', 'is_first_comment', 'post_type',
             'author_trades', 'total_comment', 'first_level_replies', 'comment_permalink', 'post_title', 'post_id',
             'comment_score', 'post_score', 'post_upvote_ratio', 'content'])
post_data = pd.DataFrame(
    columns=['author', 'created_utc', 'post_title', 'post_type', 'author_trades', 'total_comment',
             'first_level_replies', 'permalink', 'id', 'post_score', 'post_upvote_ratio', 'hwsbot_response_time',
             'is_post_deleted', 'content'])
post_count = 0
display_total_count = 0
start_epoch = int(datetime.datetime(2020, 7, 1).timestamp())

for submission in api.search_submissions(after=start_epoch,
                                         subreddit='hardwareswap',
                                         ):
    display_total_count += 1
    if submission.link_flair_text == 'OFFICIAL':
        continue
    if submission.num_comments > 0:
        submission.comment_sort = "old"

        total_comments = len(submission.comments)
        author_trades = 0

        if submission.author_flair_text and submission.author_flair_text != 'Bot':
            removed = submission.author_flair_text.replace('Trades: ', '')
            if removed.isdigit():
                author_trades = int(removed)

        seen_hwsbot = False
        first_user_comment_seen = False
        is_post_deleted = False
        bot_latency = math.nan

        if str(submission.selftext) == '[removed]':
            is_post_deleted = True

        for comment in submission.comments:
            try:
                author_trades = 0
                if comment.author_flair_text and comment.author_flair_text != 'Bot':
                    author_trades = int(comment.author_flair_text.replace('Trades: ', ''))
                latency = comment.created_utc - submission.created_utc

                if comment.is_submitter:
                    continue
                if comment.author == 'hwsbot' or comment.author == 'AutoModerator':
                    post_count += 1
                    seen_hwsbot = True
                    bot_latency = latency
                    hwsbot_response_time.at[post_count] = latency
                    if 'remove' in comment.body.lower():
                        is_post_deleted = True
                    # if first_user_comment_seen:  # we seen first user comment and hwsbot, breaking
                    #     break
                else:

                    comment_data = comment_data.append({
                        'latency': latency, 'author': str(comment.author),
                        'comment_created_utc': comment.created_utc,
                        'faster_than_hwsbot': int(not seen_hwsbot),
                        'is_first_comment': int(not first_user_comment_seen),
                        'post_type': submission.link_flair_text,
                        'author_trades': author_trades,
                        'total_comment': submission.num_comments,
                        'first_level_replies': total_comments,
                        'comment_permalink': 'https://www.reddit.com' + comment.permalink,
                        'post_title': submission.title,
                        'post_id': submission.id,
                        'comment_score': comment.score,
                        'post_score': submission.score,
                        'post_upvote_ratio': submission.upvote_ratio,
                        'is_post_deleted': int(is_post_deleted),
                        'content': str(comment.body)
                    }, ignore_index=True)
                    first_user_comment_seen = True
                    print(
                        f'{display_total_count}: Author: {comment.author} Body: {comment.body} UTC: '
                        f'{comment.created_utc} Seen hwsbot? {seen_hwsbot}')
                    # if not faster_than_hwsbot:  # we seen hwsbot since first comment is slower than hwsbot, breaking
                    #     break
            except Exception as e:
                print(f'Exception: {e}')
                print('ignoring')

        post_data = post_data.append({
            'author': str(submission.author),
            'created_utc': submission.created_utc,
            'post_title': submission.title,
            'post_type': submission.link_flair_text,
            'author_trades': author_trades,
            'total_comment': submission.num_comments,
            'first_level_replies': total_comments,
            'permalink': submission.url,
            'id': submission.id,
            'post_score': submission.score,
            'post_upvote_ratio': submission.upvote_ratio,
            'hwsbot_response_time': bot_latency,
            'content': submission.selftext
        }, ignore_index=True)

comment_data.to_csv('comment_data_july_1_jan_20.csv')
hwsbot_response_time.to_csv('hwsbot_response_time_july_1_jan_20.csv')
comment_data
