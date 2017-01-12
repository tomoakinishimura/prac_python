import requests
import lxml.html


def main():
  """
  クローラーメインの処理
  """

  response = requests.get('https://gihyo.jp/dp')
  
  #ここで関数を呼ぶ
  urls = scrape_list_page(response)
  for url in urls:
    print(url)


def scrape_list_page(response):
  root = lxml.html.fromstring(response.content)
  root.make_links_absolute(response.url)

  a_list = root.cssselect('#listBook a[itemprop="url"]')
  for a in a_list:
    url = a.get('href')
    yield url


if __name__ == '__main__':
  main()

