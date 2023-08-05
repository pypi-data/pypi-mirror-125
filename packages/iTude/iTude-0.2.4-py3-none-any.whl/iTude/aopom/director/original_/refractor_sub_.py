#!/usr/bin/python
#coding: UTF-8

from threading import Thread

#
class VTGThread_refractor_sub(Thread):
    # 2021.1.22 refractor_sub
    # 2021.1.20 refractor
    # 2020.7.4  reflection_deco
    # 2020.2.19 replace with def __init__(self, thread_name, delay, devicename, deviceorg):
    # 2020.2.14 thread adding with devicetypelist 
    #

    def __init__(self, *args, **kwargs):
        # implict self.__gNum_of_thread = 10000000
        # implict self.__delay
        # implict self.__deviceName
        # implict self.__deviceOrg
        # implict self.__iThread
        super().__init__(name = kwargs['thread_name'])


