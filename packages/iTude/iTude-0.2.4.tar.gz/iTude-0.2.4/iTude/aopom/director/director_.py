#!/usr/bin/python
#coding: UTF-8


class Versadirector:
    def __init__(self, URL, AUTH):
        self.__url = URL
        self.__auth = AUTH
    def __call__(self, func):
        def inner_wrapper(*args, **kwargs):
            #print("[Versadirector %s ] %s" % (self.__url, self.__auth))
            kwargs['url'] = self.__url
            kwargs['auth'] = self.__auth
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
