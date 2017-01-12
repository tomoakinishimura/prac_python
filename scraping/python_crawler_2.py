import requests
import lxml.html

response = requests.get('https://gihyo.jp/dp')
root = lxml.html.fromstring(response.content)
root.make_links_absolute(response.url)

a_list = root.cssselect('#listBook a[itemprop="url"]');
for a in a_list:
  url = a.get('href')
  print(url)


