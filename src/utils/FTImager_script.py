from pywinauto.application import Application
import pyautogui
import sys
import win32api
import time
import os
import ctypes

new_drives = []

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
    hwnd = ctypes.windll.user32.FindWindowW(None, title)
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 9)  
        ctypes.windll.user32.SetForegroundWindow(hwnd)


def unmount_images():
    bring_window_to_front("AccessData FTK Imager 4.7.1.2")
    bring_window_to_front("Mount Image To Drive")
    select_unmount_images(len(new_drives)+2)


def mount():
    user_input = input("Mount image automatically? N/y: ")
    if user_input.lower() == 'y':
        image_location = input("Path to image: ")
        app = Application().start(r"C:\Program Files\AccessData\FTK Imager\FTK Imager.exe")
        print("[+] FTK Imager opened")
        ftkOpen = app.window(title_re=".*AccessData*") 
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]


        if ftkOpen.wait(wait_for = 'active', timeout = 20, retry_interval = 5):
            pyautogui.hotkey('alt','f')
            for i in range(2):
                pyautogui.hotkey('down')
            pyautogui.hotkey('enter')
            print("[+] Ready for mounting image")
            pyautogui.typewrite(image_location)
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
    return user_input
            