import sys
from urllib.request import urlopen

f = urlopen('https://gihyo.jp/dp')
#HTTPヘッダーからエンコーディングを取得する
encoding = f.info().get_content_charset(failobj="utf-8")
print('encoding:', encoding, file=sys.stderr)

text = f.read().decode(encoding)
print(text)

