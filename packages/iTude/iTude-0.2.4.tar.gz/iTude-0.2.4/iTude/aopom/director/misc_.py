#!/usr/bin/python
#coding: UTF-8
import datetime

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

