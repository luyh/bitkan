

url = 'https://wapi.bitkan.pro/v2/shift/price/m_source_depth?id=1&locale=zh'

import requests

r = requests.get(url)
print(r.json())

url = 'https://wapi.bitkan.pro/v2/shift/price/m_price?locale=zh'
r = requests.get(url)
print(r.json())