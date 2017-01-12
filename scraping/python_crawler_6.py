import time
import re
import requests
import lxml.html

from pymongo import MongoClient

def main():

  client = MongoClient('localhost', 27017)
  collection = client.scraping.ebooks
  collection.create_index('key', unique=True)

  response = requests.get('https://gihyo.jp/dp')
  urls = scrape_list_page(response)
  for url in urls:
    
    key = extract_key(url)
    ebook = collection.find_one({'key': key})
    
    if not ebook:
      time.sleep(1)
      response = requests.get(url)
      ebook = scrape_detail_page(response)
      collection.insert_one(ebook)

    print(ebook)


def scrape_list_page(response):
  root = lxml.html.fromstring(response.content)
  root.make_links_absolute(response.url)

  a_list = root.cssselect('#listBook a[itemprop="url"]')
  for a in a_list:
    url = a.get('href')
    yield url

def scrape_detail_page(response):
  root = lxml.html.fromstring(response.content)
  ebook = {
    'url': response.url
    ,'title': root.cssselect('#bookTitle')[0].text_content()
    ,'price': root.cssselect('.buy')[0].text
    ,'content': [normalize_space(h3.text_content()) for h3 in root.cssselect('#content > h3')]
    ,
  }
  return ebook

def extract_key(url):
  """
  URL$B$+$i%-!<$rH4$-=P$9(B
  """
  m = re.search(r'/([^/]+)$', url)
  return m.group(1)


def normalize_space(s):
  return re.sub(r'\s+', ' ', s).strip()


if  __name__ == '__main__':
  main()

