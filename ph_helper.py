import re
import sys
import pyautogui
import win32clipboard
import pyperclip

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

def getClipboardData():
    # win32clipboard.OpenClipboard()
    # data = win32clipboard.GetClipboardData()
    # win32clipboard.CloseClipboard()
    return pyperclip.paste()

def validateClipboard():
    clipboardData = getClipboardData()
    # print ('Clipboard Data: {}'.format(clipboardData))
    pattern = re.search(r'\d+/\d+/\d+\s*\d+:\d+:\d+\s*(PM{1}|AM{1})\s+\d+\.\d+', clipboardData)
    if pattern:
        return pattern.group(0)
    else:
        print("Error: Please make sure the paraly sw 112 is logging in the center of the screen")
        sys.exit()


def goToBottom():
    copy()
    previous_data = getClipboardData()
    current_data = previous_data
    count = 0
    while previous_data == current_data:
        pyautogui.press(['down'])
        count += 1
        if count % 20 == 0:
            copy()
            previous_data = current_data
            current_data = getClipboardData()
            # print(previous_data[:30], current_data[:30])
    print("Reached Bottom")