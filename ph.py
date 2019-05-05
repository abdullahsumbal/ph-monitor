"""
Import libraries
"""
import os
import time
from ph_helper import *


# params
interval = 1


def preStartUp():
    print("*****************************************************")
    print("                     Pre-StartUp                     ")
    print("*****************************************************\n")
    # Clear up clipboard
    SetClipboard('')
    print("Pre-StartUp Done")


def startUp():
    print("*****************************************************")
    print("                     StartUp                     ")
    print("*****************************************************\n")
    print("Please read the instructions before continuing")
    print("1. Some instructions")
    print("2. More instructions")
    os.system('pause')
    print("Starting Process . . . ")
    time.sleep(5)

def isParalyCentered():

    goCenterOfScreen()
    copy()
    validateClipboard()

def isParalyLogging():
    goCenterOfScreen()
    copy()
    data = GetClipboardData()
    time.sleep(interval + 0.1)
    copy()
    if data != GetClipboardData():
        print("Paraly SW 112 is Logging")
    else:
        print("Error: Please make sure that paraly sw 112 is logging")
        sys.exit()


def isParalyRunning():
    print("*****************************************************")
    print("               Check Paraly SW 112                   ")
    print("*****************************************************\n")
    isParalyCentered()
    isParalyLogging()
# # Check if got the correct content
# isBottom = False
#
#
# print(data)
# # while not isBottom:
# #     pyautogui.press(['down'])
# #     pyautogui.hotkey('ctrl', 'c')
# #     time.sleep(5)
if __name__ == '__main__':
    preStartUp()
    startUp()
    isParalyRunning()
