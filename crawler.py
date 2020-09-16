import praw
import json
import yake
from Cleaner import Cleaner


text_content = """
Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning
competitions. Details about the transaction remain somewhat vague , but given that Google is hosting
its Cloud Next conference in San Francisco this week, the official announcement could come as early
as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the
acquisition is happening. Google itself declined 'to comment on rumors'.
"""


def create_reddit_object(json_file="reddit_config.json", json_key="reddit_user_values"):
    with open(json_file) as f:
        data = json.load(f)
        user_values = data[json_key]
        reddit = praw.Reddit(client_id=user_values['client_id'],
                             client_secret=user_values['client_secret'],
                             user_agent=user_values['user_agent'],
                             username=user_values['username'],
                             password=user_values['password'])
        return reddit


reddit = create_reddit_object()

url = "https://www.reddit.com/r/uwaterloo/comments/h9874q/is_it_really_a_sunday_unless_you_waste_the_day/"
submission = reddit.submission(url=url)

sublist = submission.selftext
submission.comments.replace_more(limit=None)
for comment in submission.comments.list():
    sublist += ' ' + comment.body

cleaner= Cleaner()
sublist= cleaner.clean_text(sublist)
simple_kwextractor = yake.KeywordExtractor(n=2)
keywords = simple_kwextractor.extract_keywords(sublist)
#for kw in keywords:
    #print(kw)

simple_kwextractor = yake.KeywordExtractor(n=2)
keywords = simple_kwextractor.extract_keywords(cleaner.clean_text(submission.title + ' ' + sublist))
for kw in keywords:
    print(kw)