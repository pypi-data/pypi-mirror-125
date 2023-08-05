#!/usr/bin/python
#coding: UTF-8


# 2021.1.3 Hyper Bound Query Director
class HBQDirector:
    def __init__(self, URL, AUTH, PORT):
        self.__url = URL
        self.__auth = AUTH
        self.__port = PORT

    def __call__(self, func):
        def inner_wrapper(*args, **kwargs):
            #print("[HBQDirector %s ] %s" % (self.__url, self.__auth, self.__port))
            kwargs['url'] = self.__url
            kwargs['auth'] = self.__auth
            kwargs['port'] = self.__port
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

