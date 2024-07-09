from pywinauto.application import Application
from pywinauto.uia_element_info import UIAElementInfo
import pyautogui
import sys
import win32api
import time
import os
import ctypes


def find_new_drives():
    drives = []
    for drive_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if os.path.exists(f'{drive_letter}:'):
            drives.append(drive_letter+":\\")
        else:
            pass
    return drives


def close_window(number: int):
    for i in range(number):
      pyautogui.hotkey('ctrl','w')


def select_unmount_images(number: int):
    pyautogui.hotkey('tab')
    for i in range(number):
       pyautogui.hotkey('shift','down')
    pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')


def bring_window_to_front(title):
    '''
    With ctypes I can interact with Windows API
    '''
    hwnd = ctypes.windll.user32.FindWindowW(None, title)
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 9)  
        ctypes.windll.user32.SetForegroundWindow(hwnd)


def unmount_images():
    bring_window_to_front("AccessData FTK Imager 4.7.1.2")
    bring_window_to_front("Mount Image To Drive")
    select_unmount_images(len(new_drives)+2)


def parse_new_drivers(drivers):
    for drive in drivers:


if len(sys.argv) != 2: 
    print("Correct usage of application: py script.py <image location> ")
    exit()
arguments = sys.argv


app = Application().start("E:\\FTK\\FTK Imager\\FTK Imager.exe")
print("[+] FTK Imager opened")
ftkOpen = app.window(title_re=".*AccessData*") 
drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]


if ftkOpen.wait(wait_for = 'active', timeout = 20, retry_interval = 5):
    pyautogui.hotkey('alt','f')
    for i in range(3):
        pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    print("[+] Ready for mounting image")
    pyautogui.typewrite(arguments[1])
    for i in range(4):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')
    print("[+] Wainting for images to be mounted...")
    time.sleep(50)

    new_drives = find_new_drives()
    if len(new_drives):
        new_drives = [drive for drive in new_drives if drive not in drives]
        print("[+] Image mounted")
        print(f"[+] The new drives are: {new_drives}")
        unmount_images()
    else:
        print("[+] No image mounted")
