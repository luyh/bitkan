from chrome.connect_chrome import Chrome
import os,time
import threading
import json

class Bitkan(Chrome):
    def __init__(self,name = 'bitkan',debug = False,mobileEmulation = None):
        self.name = name
        self.driver = None
        self.threadLock = threading.Lock()

        self.start_url = 'https://bitkan.pro/zh/trade/btc_usdt'
        self.cookies = None

    def login(self):
        self.driver.get(self.start_url)
        print('请检查自行登陆')

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        jsonCookies = json.dumps(cookies)
        with open('cookies.json', 'w') as f:
            f.write(jsonCookies)

        return jsonCookies

    def load_cookies(self):
        self.driver.get(self.start_url)
        self.driver.delete_all_cookies()

        with open('cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            self.driver.add_cookie({
                'domain': cookie['domain'],
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None
            })
        self.driver.refresh()

    def get_price(self):
        #todo:获取并解析所有行情数据，包括交易所，报价，数量，成交历史
        ask = self.driver.find_element_by_css_selector(
            'div.bktrade-component-handicap-asks.ng-star-inserted > div > div:nth-child(25) > div.bktrade-component-handicap-tr-td.bktrade-component-handicap-logo > span').text
        bid = self.driver.find_element_by_css_selector(
            'div.bktrade-component-handicap-bids.ng-star-inserted > div > div:nth-child(1) > div.bktrade-component-handicap-tr-td.bktrade-component-handicap-logo > span').text

        return float(ask) , float(bid)

    def trade(self,type,price,amount):

        price_input_xpath = '//bktrade-response-tab[{}]/div/div[2]/bktrade-component-action-pane/bk-form/form/div[2]/bk-input/div/div/input'.format(1 if type=='buy' else 2)
        amount_input_xpath = '//bktrade-response-tab[{}]/div/div[2]/bktrade-component-action-pane/bk-form/form/div[3]/bk-input/div/div/input'.format(1 if type=='buy' else 2)
        value_input_xpath = '//bktrade-response-tab[{}]/div/div[2]/bktrade-component-action-pane/bk-form/form/div[5]/bk-input/div/div/input'.format(1 if type=='buy' else 2)
        confirm_xpath = '//div/bktrade-response-tab[{}]/div/div[2]/bktrade-component-action-pane/bk-form/form/div[6]/bk-button/button'.format(1 if type=='buy' else 2)

        price_input = self.driver.find_element_by_xpath(price_input_xpath)
        amount_input = self.driver.find_element_by_xpath(amount_input_xpath)
        value_input = self.driver.find_element_by_xpath(value_input_xpath)
        confirm = self.driver.find_element_by_xpath(confirm_xpath)

        price_input.clear()
        price_input.send_keys(price)

        amount_input.clear()
        amount_input.click()
        amount_input.send_keys(str(amount))

        value_input.clear()
        value_input.send_keys(str(price * amount))

        confirm.click()


import time
import datetime

if __name__ == '__main__':
    #测试验证链接
    bitkan = Bitkan()
    bitkan.connectChrome()
    bitkan.login()
    time.sleep(3)

    ask, bid = bitkan.get_price()
    print(ask,bid,)

    bitkan.trade('buy',1000,0.003)
    bitkan.trade('sell',100000, 0.003)
    diffs = {}
    while True:
        try:
            ask,bid = bitkan.get_price()
            diff = round((ask-bid)/bid *100,4)
            print(ask, bid, '{}%'.format(diff))
            if diff < -0.2:
                now_time = datetime.datetime.now()
                diffs[now_time] = diff
                print('diffs',diffs)
            time.sleep(0.2)
        except:
            print('error')

    print('debug')











