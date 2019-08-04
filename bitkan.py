from chrome.connect_chrome import Chrome
import os,time
import threading
import json,pickle
import pandas as pd
from selenium.common.exceptions import *

class Bitkan(Chrome):
    def __init__(self,name = 'bitkan',debug = False,mobileEmulation = None):
        self.name = name
        self.driver = None
        self.threadLock = threading.Lock()

        self.start_url = 'https://bitkan.pro/zh/trade/LTC_USDT'
        self.cookies = None

        self.connectChrome()
        self.login()

        self.init_element()

        self.ask0_price_xpath = '//bktrade-response-tab[1]/div/div[2]/bktrade-component-handicap/div/div[2]/div/div[25]/div[1]/span'
        self.bid0_price_xpath = '//bktrade-response-tab[1]/div/div[2]/bktrade-component-handicap/div/div[3]/div/div[1]/div[1]/span'

        self.diffs0_df = pd.DataFrame()

    def init_element(self,num = 3):
        if num >0:

            try:
                self.price_input, self.amount_input, self.value_input, self.confirm = {}, {}, {}, {}
                for type in ['buy', 'sell']:
                    price_input_xpath = '//bktrade-response-tab[{}]/div/div[2]/bktrade-component-action-pane/bk-form/form/div[2]/bk-input/div/div/input'.format(
                        1 if type == 'buy' else 2)
                    amount_input_xpath = '//bktrade-response-tab[{}]/div/div[2]/bktrade-component-action-pane/bk-form/form/div[3]/bk-input/div/div/input'.format(
                        1 if type == 'buy' else 2)
                    value_input_xpath = '//bktrade-response-tab[{}]/div/div[2]/bktrade-component-action-pane/bk-form/form/div[5]/bk-input/div/div/input'.format(
                        1 if type == 'buy' else 2)
                    confirm_xpath = '//div/bktrade-response-tab[{}]/div/div[2]/bktrade-component-action-pane/bk-form/form/div[6]/bk-button/button'.format(
                        1 if type == 'buy' else 2)

                    self.price_input[type] = self.driver.find_element_by_xpath(price_input_xpath)
                    self.amount_input[type] = self.driver.find_element_by_xpath(amount_input_xpath)
                    self.value_input[type] = self.driver.find_element_by_xpath(value_input_xpath)
                    self.confirm[type] = self.driver.find_element_by_xpath(confirm_xpath)
            except:
                time.sleep(2)
                self.init_element(num-1)
        else:
            print('try init element error')
            exit()

    def login(self):
        self.driver.get(self.start_url)
        print('请检查登陆')
        time.sleep(3)


    def get_cookies(self):
        self.driver.get(self.start_url)
        time.sleep(3)
        self.cookies = self.driver.get_cookies()
        with open('cookies.pkl', 'wb') as f:
            pickle.dump(self.cookies,f)
        print('get cookies done')


    def add_cookies(self):
        self.driver.get(self.start_url)
        time.sleep(3)
        self.driver.delete_all_cookies()

        with open('cookies.pkl', 'rb') as f:
            self.cookies = pickle.load(f)
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)

        print('add cookies done')

    def get_price(self):
        #todo:获取并解析所有行情数据，包括交易所，报价，数量，成交历史
        self.threadLock.acquire()
        try:
            ask0_element = self.driver.find_element_by_xpath(self.ask0_price_xpath)
            bid0_element = self.driver.find_element_by_xpath(self.bid0_price_xpath)

            self.threadLock.release()

            self.ask0 = float(ask0_element.text)
            self.bid0 = float(bid0_element.text)

            self.diff0 = round((self.ask0 - self.bid0) / self.bid0 * 100, 4)

            print(self.ask0, self.bid0, '{}%'.format(self.diff0))

            if self.diff0 < -0.2:
                dict = [{
                    'time': datetime.datetime.now(),
                    'ask0': self.ask0,
                    'bid0': self.bid0,
                    'diff0': self.diff0
                }]
                diff_df = pd.DataFrame(dict)
                self.diffs0_df = pd.concat([self.diffs0_df, diff_df])
                self.diffs0_df.to_csv('diffs0.csv')
                print('update diffs0.csv')

        except StaleElementReferenceException as e:
            print('get price error', e)

    def get_price_thread(self,delay = 0.5):
        while True:
            self.get_price()
            time.sleep(delay)

    def trade(self,type,price,amount):
        self.threadLock.acquire()

        self.price_input[type].clear()
        self.price_input[type].send_keys(price)

        self.amount_input[type].clear()
        self.amount_input[type].click()
        self.amount_input[type].send_keys(str(amount))

        self.value_input[type].clear()
        self.value_input[type].send_keys(str(price * amount))

        self.confirm[type].click()

        self.threadLock.release()

import time
import datetime

if __name__ == '__main__':
    #测试验证链接
    bitkan = Bitkan()

    get_price_thread = threading.Thread(target=bitkan.get_price_thread,args=(0.5,))
    get_price_thread.start()

    bitkan.trade('buy',1000,0.003)
    time.sleep(1)
    bitkan.trade('sell',100000, 0.003)

    diffs = {}
    while True:
        try:
            ask,bid = bitkan.get_price()

        except:
            print('error')

    print('debug')











