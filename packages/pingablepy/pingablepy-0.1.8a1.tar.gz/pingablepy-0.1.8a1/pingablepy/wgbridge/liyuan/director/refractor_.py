#!/usr/bin/python
#coding: UTF-8

from threading import Thread

'''
def threadTab(**kwargs):
    delay = "0"
    thread_post = threadItem
    refrac = VTGThread_refractor(thread_name = ("%s" % thread_post))
    refrac.__setattr__("delay", delay)
    refrac.__setattr__("text_intf_", text_intf_)
    refrac.__setattr__("text_intf_brief_", text_intf_brief_)
    refrac.__setattr__("butt", threadItem)
    refrac.__setattr__("dev", dev)
    refrac.__setattr__("hostName", hostName)
    refrac.__setattr__("deviceName", deviceName)
    refrac.__setattr__("deviceOrg", deviceOrg)
    refrac.__setattr__("contents", contents)
    refrac.__setattr__("ala", ala)
    return refrac

'''

#
class VTGThread_refractor(Thread):
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


