from selenium import webdriver
import json
from celery import Celery
import concurrent.futures

JSON_FILE='tag_url.json'
#app = Celery('tasks', broker='amqp://localhost//')

titles=[]
def scraper(url):
    driver = webdriver.Firefox()
    driver.get(url)
    titles.append(driver.title)
    driver.close()

with open(JSON_FILE) as f:
    categories = json.load(f)
    for category_key in categories:
        collection = categories[category_key]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            res = executor.map(lambda category,url:scraper(url),collection.items())


