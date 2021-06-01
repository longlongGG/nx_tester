#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Dragon
# @Software: PyCharm
from selenium import webdriver
class Testkeywords(object):
    def __init__(self,url,browser_type):
        self.driver =self.open_browser(browser_type)
        self.driver.get(url)
    def open_browser(self,browser_type):
        if browser_type == 'chrome':
            driver = webdriver.Chrome()
            return driver
        elif browser_type == 'firefox':
            driver = webdriver.Firefox()
            return driver
        else:
            print('error')
    def locater(self,locator_type,value):
        if locator_type == 'xpath':
            el =  self.driver.find_element_by_xpath(value)
            return el
        elif locator_type == 'id':
            el = self.driver.find_element_by_id(value)
            return el
        elif locator_type == 'name':
            el = self.driver.find_element_by_name(value)
            return el

    def inputs(self,locator_type,xpath_value,value):
        self.locater(locator_type,xpath_value).send_keys(value)

    def click_but(self,locator_type,xpath_value):
        self.locater(locator_type,xpath_value).click()
    def quit_brower(self):
        self.driver.quit()


# if __name__ == '__main__':
#     tk = Testkeywords('https://www.baidu.com/','chrome')
#     tk.inputs('id','kw','虚竹')
#     tk.click_but('xpath','//*[@id="su"]')
