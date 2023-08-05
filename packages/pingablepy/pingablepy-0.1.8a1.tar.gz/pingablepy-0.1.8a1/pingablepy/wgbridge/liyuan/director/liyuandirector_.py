#!/usr/bin/python
#coding: UTF-8

import requests
from requests.adapters import HTTPAdapter
from collections import Counter
import datetime
from urllib.parse import urljoin
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import os, pickle
import json, time

# 2021.8.31 casebook
# 2021.8.5  seco_str
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
            ## sess.mount('http://', HTTPAdapter(max_retries = maxRetries))
            sess.mount('https://', HTTPAdapter(max_retries = maxRetries))
            # BASE_URL = self.__url + ":" + self.__port
            try:
                sess.get(url = f"https://{self.__urlw.most_common(1)[0][0]}:{self.__port}", timeout = timeOut, verify = False)
            except requests.exceptions.ConnectionError as e:
                print(f"! Fail to connect, this {(self.__urlw.most_common(1)[0][0])} could be blocked or delay ")
                self.__urlw.subtract([self.__urlw.most_common(1)[0][0]])
            kwargs['url'] = f"https://{(self.__urlw.most_common(1)[0][0])}"
            kwargs['auth'] = self.__auth
            kwargs['port'] = self.__port
            print(f"- Connected {(kwargs['url'])}")
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
        return inner_wrapper
    return wrapper


def secit():
    """
    Count the function in seconds
    """
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            sT = datetime.datetime.now() #start = time.clock()
            func(*args, **kwargs)
            eT = datetime.datetime.now() # print('{} sec'.format((eT - sT)))
            print(f" {(eT - sT)} sec ") #end = time.clock() #print('used: {}'.format(end - start))
        return inner_wrapper
    return wrapper


seco_string_ = "parameter: secotime"
def seco_str(*dargs, **dkwargs):
    """
    Count the function in seconds
    """
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            sT = datetime.datetime.now()
            func(*args, **kwargs)
            eT = datetime.datetime.now()
            # print(dargs) # print(dkwargs) # print(f" {(eT - sT)} sec ")
            outseco_ = str(f" {(eT - sT)} sec ") # secotime_ = str(f" {(eT - sT).seconds} sec ")
            print(" -- -- -- -- -- ")
            print(f' {(outseco_)} ')
        return inner_wrapper
    return wrapper

def step_str(*dargs, **dkwargs):
    """
    Count the function in number
    """
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            func(*args, **kwargs)
            outinc_ = str(f" The Step {inc()} Done ")
            print(" -- -- -- -- -- ")
            print(f' {(outinc_)} ')
        return inner_wrapper
    return wrapper

def inc():
    def counter():
        count = 0
        while True:
            count += 1
            response = yield count
            if response is not None:
                count = response
    c = counter()
    return lambda x = False: c.send(0) if x else next(c)


 