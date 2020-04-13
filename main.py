import os
from crawler import VOJCrawler
from crawler.SPOJCrawler import SPOJCrawler
current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)

BASE_URL = 'https://vn.spoj.com/'

crawler = SPOJCrawler(BASE_URL,
                      BASE_URL + 'files/src/save/{id}')
