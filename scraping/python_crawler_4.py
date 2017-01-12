import requests
import lxml.html
import re

def main():
  """
  メイン関数
  """

  session = requests.Session()
  response = requests.get('https://gihyo.jp/dp')
  urls = scrape_list_page(response)
  for url in urls:
    response = session.get(url)
    ebook = scrape_detail_page(response)
    print(ebook)
    break#ひとまず1ページ分だけ


def scrape_list_page(response):
  """
  一覧データの取得
  """
  root = lxml.html.fromstring(response.content)
  root.make_links_absolute(response.url)

  a_list = root.cssselect('#listBook a[itemprop="url"]')
  for a in a_list:
    url = a.get('href')
    yield url

def scrape_detail_page(response):
  """
  詳細ページのレスポンスから電子書籍の情報をdictで取得する
  """
  root = lxml.html.fromstring(response.content)
  ebook = {
    'url': response.url
    ,'title': root.cssselect('#bookTitle')[0].text_content()
    ,'price': root.cssselect('.buy')[0].text
    ,'content': [normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')]
    ,
  }
  return ebook


def normalize_spaces(s):
  return re.sub(r'\s+', ' ', s).strip()

if __name__ == '__main__':
  main()
