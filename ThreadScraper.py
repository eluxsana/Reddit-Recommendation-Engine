import pandas as pd
import json
from SearchGenerator import SearchGenerator
import concurrent.futures
import openpyxl
import time
import praw
import os
import numpy as np
from Cleaner import Cleaner

start_time = time.time()


class ThreadScraper:
    def __init__(self, url):
        self.res_dict = {'Title': [],
                         'Content': [],
                         'Title + Content':[],
                         'URL': [],
                         'ID': []}
        self.url = url
        self.sg = SearchGenerator(self.url)
        self.search_terms = np.asarray(self.sg.extract_keywords())
        self.df=''
        self.cleaner = Cleaner()

    def get_submissions(self,term):
        submissions = self.sg.get_reddit().subreddit(str(self.sg.get_subreddit())).search(term[0], time_filter='year',syntax='plain')
        for sub in submissions:
            title = sub.title
            content = sub.selftext
            url = sub.url
            id = sub.id
            if not (url.endswith(".jpg")) and not (url.endswith(".png")) and not (url.endswith(".gif")) and len(
                content) > 50 and ('http' not in content) and (id not in self.res_dict['ID']):
                self.res_dict['Title'].append(self.cleaner.clean_text(title).split())
                self.res_dict['Content'].append(self.cleaner.clean_text(content).split())
                self.res_dict['Title + Content'].append(self.cleaner.clean_text(title + ' ' + content).split())
                self.res_dict['URL'].append(url)
                self.res_dict['ID'].append(id)

    def export_submission(self):
        with concurrent.futures.ThreadPoolExecutor(8) as executor:
            executor.map(self.get_submissions, self.search_terms)
        df = pd.DataFrame(self.res_dict)
        df.dropna(inplace=True)
        df.reset_index()
        self.df = df
        if not os.path.exists('data'):
            os.makedirs('data')
        print("Writing to CSV")
        df.to_csv('data/results.csv')
        print("Done...")
        return df




