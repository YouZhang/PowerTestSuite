#coding = utf-8

import win32api
import win32con
import time
from ctypes import *
import os

localTime = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())

def appendLog(message,folder="Log"):
    print message
    logfile = getDir(folder,localTime+".log")
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

def cmdRun(cmd):
    appendLog("running command : %s" % cmd)
    os.system(cmd)

def mkdir(path):
    appendLog("make directory %s" % path)
    try:
        os.mkdir(path)
    except WindowsError:
        appendLog("%s folder has been exsited" % path)

def getDir(*path):
    return os.path.join(*path)

def removeFiles(patten,path=None):
    assert (patten != None)
    if( path != None ):
        targetFiles = getDir(path,patten)
    else:
        targetFiles = patten
    appendLog("removing files : %s" % patten)
    cmdRun("del %s" % targetFiles)

def copy(src,target):
    appendLog("copy /y files from : %s to %s" % (src,target))
    cmdRun("copy %s %s" % (src,target))

def move(src,target):
    appendLog("move files from %s to %s" % (src,target))
    cmdRun("move %s %s" % (src,target))

def syncRun(fileName):
    cmd = 'start ' + fileName
    cmdRun(cmd)

def syncAdminRun(fileName):
    cmd = 'runas /savecred /user:administrator ' + fileName
    cmdRun(cmd)

def getIp(machineName,mode=""):
    resultFile = mode + "_pingRes.txt"
    cmdRun("ping %s > %s" % (machineName,resultFile))
    handle = open(resultFile,'r')
    line = handle.readline()
    if(line == '\n'):
        line = handle.readline()
        try:
            startPos = line.index('[')
            endPos = line.index(']')
            ip = line[startPos+1:endPos]
            if(len(ip) < 10):
                appendLog("cannot find your ip")
                return -1
            return ip
        except:
            appendLog("could not find the server ip, pls check the network config")
            return -1

if __name__ == "__main__":
    mouseClick(65,55)
    time.sleep(10)
    mouseClick(110,55)