import nltk
import praw
import json
from Cleaner import Cleaner
import yake

class SearchGenerator:
    def __init__(self, url):
        self.url = url
        self.reddit = self.create_reddit()
        self.submission = self.reddit.submission(url=url)

    def create_reddit(self, json_file="reddit_config.json", json_key="reddit_user_values"):
        with open(json_file) as f:
            data = json.load(f)
            user_values = data[json_key]
            reddit = praw.Reddit(client_secret=user_values['client_secret'],
                                 client_id=user_values['client_id'],
                                 user_agent=user_values['user_agent'],
                                 username=user_values['username'],
                                 password=user_values['password'])
            return reddit

    def get_title(self):
        return self.submission.title

    def get_body(self):
        return self.submission.selftext

    def get_subreddit(self):
        return self.submission.subreddit

    def get_reddit(self):
        return self.reddit

    def get_comments(self):
        text = ""
        self.submission.comments.replace_more(limit=None)
        for comment in self.submission.comments.list():
            text += ' ' + comment.body
        return text

    def scrape_submission(self):
        text = self.get_title()
        text += ' ' + self.get_body()
        if len(text) <= 1000:
            text += ' ' + self.get_comments()
        return text

    def get_cleantext(self, text):
        cleaner = Cleaner()
        cleaned = cleaner.clean_text(text)
        return cleaned

    def get_cleancontent(self):
        return self.get_cleantext(self.scrape_submission())

    def extract_keywords(self):
        content= self.get_cleantext(self.scrape_submission())
        kwextractor1 = yake.KeywordExtractor(n=1)
        keywords1 = kwextractor1.extract_keywords(content)
        kwextractor2 = yake.KeywordExtractor(n=2)
        keywords2 = kwextractor2.extract_keywords(content)
        final=keywords1[:5] + keywords2[:5]
        return final
