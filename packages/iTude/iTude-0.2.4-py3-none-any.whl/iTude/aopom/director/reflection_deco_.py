#!/usr/bin/python
#coding: UTF-8

import threading

#vtg_reflection_deco_ = []
#vtg_reflection_deco_set = set()

#
class VTGThread_reflectionDeco(threading.Thread):
    # 2020.7.4  reflection_deco
    # 2020.2.19 replace with def __init__(self, thread_name, delay, devicename, deviceorg):
    # 2020.2.14 thread adding with devicetypelist 
    #

    def __init__(self, *args, **kwargs):
        super().__init__(name = kwargs['thread_name'])
