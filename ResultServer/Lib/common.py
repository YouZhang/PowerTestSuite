#coding = utf-8

import win32api
import win32con
import time
from ctypes import *
import os

localTime = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())

def appendLog(message):
    print message
    logfile = os.path.join("Log",localTime+".log")
    logHandle = open(logfile,"a")
    logHandle.write(message + "\n\n")
    logHandle.close()

def mouseMove(x,y):
    windll.user32.SetCursorPos(x,y)

def mouseClick(x,y):
    if not x is None and not y is None:
        mouseMove(x,y)
        time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    time.sleep(0.01)


if __name__ == "__main__":
    mouseClick(65,55)
    time.sleep(10)
    mouseClick(110,55)