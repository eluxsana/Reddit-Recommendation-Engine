# Import libraries
import pickle
from gensim import models, similarities


#url = "https://www.reddit.com/r/relationship_advice/comments/hc7p4w/update_i_30f_found_out_my_husband_32m_hired_my/"
# Import modules
from Cleaner import Cleaner
from ThreadScraper import ThreadScraper
from SearchGenerator import SearchGenerator

class Evaluate:
    def __init__(self,url):
        self.url=url
        self.ts=ThreadScraper(url)
        self.df=self.ts.export_submission()
        print(self.df.to_string())
        # Database and other resources
        LDA_PATH = "data/lda_model"
        DICTIONARY_PATH = "data/dictionary"
        CORPUS_PATH = "data/corpus"
        # Load all respources
        with open(DICTIONARY_PATH, 'rb') as fp:
            self.dictionary = pickle.load(fp)
            fp.close()
        with open(CORPUS_PATH, 'rb') as fp:
            self.corpus = pickle.load(fp)
            fp.close()
        self.lda = models.LdaModel.load(LDA_PATH)

    def get_similarity(self,lda, query_vector):
        index = similarities.MatrixSimilarity(lda[self.corpus])
        sims = index[query_vector]
        return sims
    def get_recommendations(self):
        cleaner = Cleaner()
        sg=SearchGenerator(self.url)
        words = self.dictionary.doc2bow(sg.get_cleancontent().split())
        print("Top words identified: ")
        for word in words:
            print("{} {}".format(word[0], self.dictionary[word[0]]))
        query_vector = self.lda[words]
        sims = self.get_similarity(self.lda, query_vector)
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        idx = 0
        pids = []
        result = 10
        recommendation=[]
        page_ids = self.df['ID'].to_list()
        print("\nCheck out the links below:")
        while result > 0:
            pageid = page_ids[sims[idx][0]]
            if pageid not in pids:
                pids.append(pageid)
                print("{}".format(self.df[self.df['ID']==pageid]['URL'].values[0]))
                recommendation.append(self.df[self.df['ID']==pageid]['URL'].values[0])
                result -= 1
            idx += 1
        return recommendation

#ev=Evaluate(url)
#r=ev.get_recommendations()
#open('Extension/result.txt', 'w').close()
#with open('Extension/result.txt','a') as f:
#    for i in r:
 #       f.write(i+'\n')


