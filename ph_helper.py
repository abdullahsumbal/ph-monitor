import re
import sys
import pyautogui
import win32clipboard

####################################################
# mouse and keyboard automation function
####################################################

def goCenterOfScreen():
    # Go to the center of the screen
    screenWidth, screenHeight = pyautogui.size()

    # Mouse left click
    pyautogui.click(screenWidth / 2, screenHeight / 2)


def copy():
    # Copy row (ctrl + c)
    pyautogui.hotkey('ctrl', 'c')

####################################################
# Clipboard helper function
####################################################
def SetClipboard(data):
    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()

def GetClipboardData():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data

def validateClipboard():
    clipboardData = GetClipboardData()
    print ('Clipboard Data: {}'.format(clipboardData))
    pattern = re.search(r'\d+/\d+/\d+\s*\d+:\d+:\d+\s*(PM{1}|AM{1})\s+\d+\.\d+', clipboardData)
    win32clipboard.CloseClipboard()
    if pattern:
        print("Paraly sw 112 is positioned correctly")
        return pattern.group(0)
    else:
        print("Error: Please make sure the paraly sw 112 is logging in the center of the screen")
        sys.exit()

