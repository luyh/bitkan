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
        self.driver.add_cookie(self.cookies)
        url = 'https://bitkan.pro/zh/account/login'
        self.driver.get(url)
        cookies = None
        print('请自行登陆')

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
        ask = self.driver.find_elements_by_css_selector('div.bktrade-component-handicap-asks.ng-star-inserted > div > div:nth-child > div.bktrade-component-handicap-tr-td.bktrade-component-handicap-logo > span').text
        bid = self.driver.find_elements_by_css_selector('div.bktrade-component-handicap-bids.ng-star-inserted > div > div:nth-child > div.bktrade-component-handicap-tr-td.bktrade-component-handicap-logo > span').text

        return float(ask) , float(bid)

    def trade(self,type,price,amount):
        if type == 'buy':
            price_input_selector = 'div.bktrade-response-tab-content > bktrade-component-action-pane > bk-form > form > div:nth-child(2) > bk-input > div > div > input'
            amount_input_selector = 'div.bktrade-response-tab-content > bktrade-component-action-pane > bk-form > form > div:nth-child(3) > bk-input > div > div > input'
            confirm_selector = 'div.bktrade-response-tab-content > bktrade-component-action-pane > bk-form > form > div.bktrade-component-action-pane-submit > bk-button > button'
        elif type == 'sell':
            price_input_selector = 'bktrade-response-tab:nth-child(2) > div > bktrade-component-action-pane > bk-form > form > div:nth-child(2) > bk-input > div > div > input'
            amount_input_selector = 'bktrade-response-tab:nth-child(2) > div > bktrade-component-action-pane > bk-form > form > div:nth-child(3) > bk-input > div > div > input'
            confirm_selector = 'bktrade-response-tab:nth-child(2) > div > bktrade-component-action-pane > bk-form > form > div.bktrade-component-action-pane-submit > bk-button > button'
        else:
            print('trade type error')
            return

        price_input = self.driver.find_element_by_css_selector(price_input_selector)
        amount_input = self.driver.find_element_by_css_selector(amount_input_selector)
        confirm = self.driver.find_element_by_css_selector(confirm_selector)

        price_input.clear()
        price_input.click()
        price_input.send_keys(price)

        amount_input.clear()
        amount_input.click()
        amount_input.send_keys(str(amount))

        confirm.click()


import time
import datetime

if __name__ == '__main__':
    #测试验证链接
    bitkan = Bitkan()
    bitkan.connectChrome()
    bitkan.login()
    time.sleep(3)

    cookies = bitkan.driver.get_cookies()
    print(cookies)

    bitkan.driver.delete_all_cookies()

    bitkan.driver.add_cookie(cookies)



    bitkan.trade('buy',1000,0.001)
    bitkan.trade('sell',100000, 0.001)
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











