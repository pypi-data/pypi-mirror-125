# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--disable-infobars')


class BasePageObject():

    def __init__(self):
        self.__driverpath = "E:\\ProgramData\\Anaconda3\\chromedriver.exe"
        try:
            # self.driver = webdriver.Chrome(self.__driverpath)
            self.driver = webdriver.Chrome(self.__driverpath, chrome_options = chrome_options)
        except Exception:
            raise NameError("Not Chrome")


    def visit(self, url):
        if url != "":
            self.driver.get(url)
            self.driver.maximize_window()
            self.driver.implicitly_wait(4)
        else:
            raise ValueError("Please fetch a url path")


    def locate_element(self, *loc):
        try:
            #
            WebDriverWait(self.driver, 60, 0.1).until(EC.visibility_of_element_located(loc))
            ##return self.driver.find_element(*loc)
            ##return WebDriverWait(driver, 60, 0.1).until(EC.presence_of_element_located((By.XPATH, workflows_xpath)))
            return WebDriverWait(self.driver, 60, 0.1).until(EC.presence_of_element_located(loc))
        except:
            # print(f' {self} On page, not found element{loc} ')
            print('{} On page, not found element {}'.format(self, loc))


    def send_keys(self, loc, value, clear_first = True, click_first = True):
        try:
            loc = getattr(self, "_%s" % loc)
            if click_first:
                self.locate_element(*loc).click()
            if click_first:
                self.locate_element(*loc).clear()
                self.locate_element(*loc).send_keys(value)
        except AttributeError:
            # print(f' {self} On page, not found element{loc} ')
            print('{} On page, not found element {}'.format(self, loc))


    def quit(self):
        self.driver.implicitly_wait(60)
        self.driver.quit()



            




