#!/usr/bin/python
#coding: UTF-8

import requests
from requests.adapters import HTTPAdapter
from collections import Counter
import datetime

# 2021.7.20 secit, pointmerge
# 2021.6.22 Multi-URL with weight update
# 2021.6.21 LIYUAN update
# 2021.4.2  Hyper Bound Query Director
# 2020.2.1  Origin
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
            maxRetries = 3
            timeOut = 6
            sess = requests.Session()
            sess.mount('http://', HTTPAdapter(max_retries = maxRetries))
            sess.mount('https://', HTTPAdapter(max_retries = maxRetries))
            # BASE_URL = self.__url + ":" + self.__port
            try:
                sess.get(url = 'https://{}:{}'.format(self.__urlw.most_common(1)[0][0], self.__port), timeout = timeOut, verify = False) # sess.get(url = "https://" + self.__urlw.most_common(1)[0][0] + ":" + self.__port, timeout = timeOut, verify = False)
            except requests.exceptions.ConnectionError as e:
                print('-- Fail to connect, this {} could be blocked or delay '.format(self.__urlw.most_common(1)[0][0]))
                self.__urlw.subtract([self.__urlw.most_common(1)[0][0]])
            kwargs['url'] = "https://{}".format(self.__urlw.most_common(1)[0][0])
            kwargs['auth'] = self.__auth
            kwargs['port'] = self.__port
            print('-- Connectable {}'.format(kwargs['url']))
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


def pointmerge(targetobject = "VTGThread_refractor", point = "run", merger = "merger"):
    """
    Pointance of merge func 
    """
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            setattr(targetobject, point, merger)
            func(*args, **kwargs)
            # '{}{}{}'.format(targetobject, point, merger)
        return inner_wrapper
    return wrapper


def secit():
    """
    Count the function in seconds
    """
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            #start = time.clock()
            sT = datetime.datetime.now()
            func(*args, **kwargs)
            eT = datetime.datetime.now()
            print('{} sec'.format((eT - sT)))
            #end = time.clock()
            #print('used: {}'.format(end - start))
        return inner_wrapper
    return wrapper



