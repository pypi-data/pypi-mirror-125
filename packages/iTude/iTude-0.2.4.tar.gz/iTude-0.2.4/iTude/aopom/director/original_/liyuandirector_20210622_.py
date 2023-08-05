#!/usr/bin/python
#coding: UTF-8

import requests
from requests.adapters import HTTPAdapter
from collections import Counter

# 2021.6.22 multi-URL with weight update
# 2021.6.21 LIYUAN update
# 2021.4.2 Hyper Bound Query Director
class LIYUANDirector:
    def __init__(self, URL, AUTH, PORT):
        self.__auth = AUTH
        self.__port = PORT
        self.__urlw = Counter(URL)

    def __call__(self, func):
        def inner_wrapper(*args, **kwargs):
            # print("[ LIYUANDirector %s ] %s" % (self.__url, self.__auth, self.__port))
            # print(args, kwargs)
            # 2021.6.21 session update into director
            # 2021.1.20 session retries(4), timeout(8)
            maxRetries = 4
            timeOut = 8
            sess = requests.Session()
            sess.mount('http://', HTTPAdapter(max_retries = maxRetries))
            sess.mount('https://', HTTPAdapter(max_retries = maxRetries))
            # BASE_URL = self.__url + ":" + self.__port
            try:
                sess.get(url = "https://" + self.__urlw.most_common(1)[0][0] + ":" + self.__port, timeout = timeOut, verify = False)
            except requests.exceptions.ConnectionError as e:
                print('fail to connect, this {} could be blocked or delay'.format(self.__urlw.most_common(1)[0][0]))
                self.__urlw.subtract([self.__urlw.most_common(1)[0][0]])
            kwargs['url'] = "https://" + self.__urlw.most_common(1)[0][0]
            kwargs['auth'] = self.__auth
            kwargs['port'] = self.__port
            print('connectable {}'.format(kwargs['url']))
            return func(*args, **kwargs)
        return inner_wrapper

    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self, URL):
        self.__url = URL
    @url.deleter
    def url(self):
        del self.__url

    @property
    def auth(self):
        return self.__auth
    @auth.setter
    def auth(self, AUTH):
        self.__auth = AUTH
    @auth.deleter
    def auth(self):
        del self.__auth

    @property
    def port(self):
        return self.__port
    @port.setter
    def port(self, PORT):
        self.__port = PORT
    @port.deleter
    def port(self):
        del self.__port

#

