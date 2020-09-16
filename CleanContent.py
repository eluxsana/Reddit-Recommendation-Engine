import pandas as pd

df = pd.read_csv('results.csv')
print(df.to_string())

from Cleaner import Cleaner
from ThreadScraper import ThreadScraper

class Content:

    def __init__(self, df,url):
        self.df = df
        self.cleaner = Cleaner()

    def clean_frame(self):
        self.df=self.df[['Title','Content']].apply(lambda x: self.cleaner.clean_text(x).split())
        
url = "https://www.reddit.com/r/uwaterloo/comments/gomj1g/how_to_get_good_algorithms_and_data_structures/"
c=Content(ThreadScraper(url).export_submission())
c.clean_frame()
print(Content.df.to_string())