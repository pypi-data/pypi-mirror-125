#!/usr/bin/python
#coding: UTF-8

import os

try:

   from colorama import init, Fore, Back, Style
   init(autoreset=True)

except ImportError:

   try:

       command_to_execute = "pip install colorama || easy_install colorama"

       os.system(command_to_execute)

   except OSError:

       print ("Can NOT install colorama, Aborted!")

       sys.exit(1)

   from colorama import init, Fore, Back, Style
   init(autoreset=True)


try:

   from pythonping import ping

except ImportError:

   try:

       command_to_execute = "pip install pythonping || easy_install pythonping"

       os.system(command_to_execute)

   except OSError:

       print ("Can NOT install pythonping, Aborted!")

       sys.exit(1)

   from pythonping import ping

# from .vtg_alarms_weakauth_ import *

def pingable_console_(server_list_object):
    print('Startup.')
    error_list = []
    # ala = VTG_alarms()
    for ip in server_list_object:
        rs = ping(ip, size = 80, count = 10)
        if 1.0 >= rs.packet_loss > 0.5:
            print(Fore.RED + f" {ip}.PacketLossRate.{rs.packet_loss*100}% ")
            # alarm_mail_print_
            error_list.append(ip)

    if 0 == len(error_list):
        print("Each IP-Ping Pass\n")
    else:
        # alarmprint_content_critical_(ala, error_list)
        print(" Alarm To Print ")

    print('.End.')
    return error_list

def alarmprint_content_critical_(ala, contents):
    # CRITICAL
    contents.append(" [ CRITICAL ] ")
    contents.append(" Descriptions: UNREACHABLE IP LIST ABOVE ! ")
    contents.append(" Powerby TSunx ")
    ala.qiye_mail_print_(contents)









