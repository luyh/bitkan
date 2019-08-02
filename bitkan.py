from chrome.connect_chrome import Chrome
import os,time
import threading


class Bitkan(Chrome):
    def __init__(self,name = 'bitkan',debug = False,mobileEmulation = None):
        self.name = name
        self.driver = None
        self.threadLock = threading.Lock()

        self.url = 'https://bitkan.com/zh/'

    def login(self):
        url = 'https://bitkan.pro/zh/trade/btc_usdt'
        self.driver.get(url)
        print('请自行登陆')

    def get_price(self):
        ask = self.driver.find_element_by_css_selector('div.bktrade-component-handicap-asks.ng-star-inserted > div > div:nth-child(25) > div.bktrade-component-handicap-tr-td.bktrade-component-handicap-logo > span').text
        bid = self.driver.find_element_by_css_selector('div.bktrade-component-handicap-bids.ng-star-inserted > div > div:nth-child(1) > div.bktrade-component-handicap-tr-td.bktrade-component-handicap-logo > span').text

        return float(ask) , float(bid)

import time
if __name__ == '__main__':
    #测试验证链接
    bitkan = Bitkan()
    bitkan.connectChrome()
    bitkan.login()
    time.sleep(3)
    while True:
        try:
            ask,bid = bitkan.get_price()
            print(ask,bid)
            time.sleep(0.2)
        except:
            print('error')

    print('debug')











