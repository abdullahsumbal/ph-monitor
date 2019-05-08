import re
import sys
import pyautogui
import pyperclip

pyautogui.FAILSAFE = True
####################################################
# mouse and keyboard automation function
####################################################


def click():
    pyautogui.click()


def moveMouse(x, y):
    pyautogui.moveTo(x, y)


def clickOnPosiiton(x , y):
    pyautogui.click(x , y)

def copy():
    # Copy row (ctrl + c)
    pyautogui.hotkey('ctrl', 'c')


def mousePosition():
    return pyautogui.position()

####################################################
# Clipboard helper function
####################################################


def SetClipboard(data):
    pyperclip.copy(data)


def getClipboardData():
    return pyperclip.paste()


def validateClipboard():
    clipboardData = getClipboardData()
    # print ('Clipboard Data: {}'.format(clipboardData))
    pattern = re.search(r'\d+/\d+/\d+\s*\d+:\d+:\d+\s*(PM{1}|AM{1})\s+\d+\.\d+', clipboardData)
    if pattern:
        return clipboardData
    else:
        print("Error: Please make sure the Cursor is placed on a row of paraly sw 112")
        sys.exit()
