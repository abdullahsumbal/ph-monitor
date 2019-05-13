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
    print("                  PH: Pre-StartUp                     ")
    print("*****************************************************\n")
    # Clear up clipboard
    SetClipboard('')
    print("Pre-StartUp Done")


def startUp():
    print("*****************************************************")
    print("                   PH: StartUp                     ")
    print("*****************************************************\n")
    print("Please read the instructions before continuing")
    print("1. After pressing enter, you will 10 seconds to perform the actions belows")
    print("2. Start logging the paraly SW 112")
    print("3. Place cursor on the bottom row on the ph value.")
    print("4. Do not move the cursor or else the program will stop")
    os.system('pause')
    print("Starting Process . . . ")
    time.sleep(10)

def get_row(x = None, y = None):
    if x and y:
        clickOnPosiiton(x, y)
    else:
        click()
    copy()
    time.sleep(0.5)
    data = validateClipboard()
    return data

def isParalyLogging():
    print("*****************************************************")
    print("               PH: Check Cursor Position")
    print("*****************************************************\n")
    print("Check if Paraly SW 112 is logging . . . \n")
    previous_row = get_row()
    time.sleep(interval *2)
    current_row = get_row()
    if( current_row != previous_row):
        print("Paraly SW 112 is logging\n")
        return mousePosition()
    else:
        print("Error: Looks like Paraly SW 112 is not logging.")
        print("How to fix: ")
        print("1. Please make sure mouse is placed on the ph value of the last row of the log.")
        print("2. You must see the time incrementing")
        sys.exit()


def getHP(phValueLocationX, phValueLocationY):

    # get current mouse position
    currentX, currentY = mousePosition()

    # go to where the ph value is on the screen
    rowData = get_row(phValueLocationX, phValueLocationY)

    # reposition mouse to the current position
    moveMouse(currentX, currentY)

    # get ph value from data
    phValue = re.findall(r'\d+\.\d+', rowData)[0]
    return phValue, rowData

time.sleep(interval)
if __name__ == '__main__':
    preStartUp()
    startUp()
    phValueLocationX, phValueLocationY = isParalyLogging()
    while(True):
        print(getHP(phValueLocationX, phValueLocationY))

