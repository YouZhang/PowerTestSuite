#coding = utf-8
import os
import re
import win32api
import win32con
import time
from win32api import GetSystemMetrics
from xml.etree import ElementTree as ET
from KeyValue import VK_CODE

class sysConfigFile(object):

    def __init__(self,xmlFile = 'sysConfig.xml'):
        self.rootNode = ET.parse(xmlFile).getroot()

    def getSysConfigItem(self,*args):
        item = self.rootNode.find(args[0])
        for i in range(1,len(args)):
            item = item.find(args[i])
        return item

    def getConfigContent(self,*args):
        item = self.getSysConfigItem(*args)
        return item.text

    def getConfigTag(self,*args):
        item = self.getSysConfigItem(*args)
        return item.tag

localTime = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())

def switchTo4K():
    win32api.keybd_event(VK_CODE['win'],0,0,0)
    win32api.keybd_event(VK_CODE['p'],0,0,0)
    win32api.keybd_event(VK_CODE['win'],0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(VK_CODE['p'],0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(1)
    win32api.keybd_event(VK_CODE['up_arrow'],0,0,0)
    win32api.keybd_event(VK_CODE['up_arrow'],0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(1)
    win32api.keybd_event(VK_CODE['enter'],0,0,0)
    win32api.keybd_event(VK_CODE['enter'],0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(12)

def switchTo1080():
    win32api.keybd_event(VK_CODE['win'],0,0,0)
    win32api.keybd_event(VK_CODE['p'],0,0,0)
    win32api.keybd_event(VK_CODE['win'],0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(VK_CODE['p'],0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(1)
    win32api.keybd_event(VK_CODE['down_arrow'],0,0,0)
    win32api.keybd_event(VK_CODE['down_arrow'],0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(1)
    win32api.keybd_event(VK_CODE['enter'],0,0,0)
    win32api.keybd_event(VK_CODE['enter'],0,win32con.KEYEVENTF_KEYUP,0)


def appendLog(message):
    print message
    logfile = os.path.join("Log",localTime+".log")
    logHandle = open(logfile,"a")
    logHandle.write(message + "\n\n")
    logHandle.close()


def parseClipInfo(clip):
    resMatchedCase = ".*_(\d+)p.*"
    fpsMatchedCase = ".*_(\d+)fps.*"
    frameMatchedCase = ".*_(\d+)frame.*"
    tenBitMatchedCase = ".*_m(\d+).*"
    try:
        resolution = matchCase(clip,resMatchedCase)
        targetFPS = matchCase(clip,fpsMatchedCase)
        frameNum = matchCase(clip,frameMatchedCase)
        tenBit = matchCase(clip,tenBitMatchedCase)
        return resolution,targetFPS,frameNum,tenBit
    except:
        appendLog("the clip name do not match the standard..please check")
        return -1

def matchCase(content,patten,pos=0):
    patten = re.compile(patten)
    matchedItem = patten.match(content,pos)
    return matchedItem.group(1)

def is4kMetric():
    width = GetSystemMetrics(0)
    appendLog("width: %s" % width)
    if(width > 1500):
        return True
    else:
        return False

def keyPress(targetStr):
    for i in range(len(targetStr)):
        target = targetStr[i].lower()
        if( ':' == target ):
            win32api.keybd_event(VK_CODE['left_shift'],0,0,0)
            win32api.keybd_event(VK_CODE[';'],0,0,0)
            win32api.keybd_event(VK_CODE['left_shift'],0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(VK_CODE[';'],0,win32con.KEYEVENTF_KEYUP,0)
        elif( '_' == target ):
            win32api.keybd_event(VK_CODE['left_shift'],0,0,0)
            win32api.keybd_event(VK_CODE['-'],0,0,0)
            win32api.keybd_event(VK_CODE['left_shift'],0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(VK_CODE['-'],0,win32con.KEYEVENTF_KEYUP,0)
        else:
            win32api.keybd_event(VK_CODE[target],0,0,0)
            win32api.keybd_event(VK_CODE[target],0,win32con.KEYEVENTF_KEYUP,0)

def syncRun(fileName):
    cmd = 'start ' + fileName
    os.system(cmd)

def syncAdminRun(fileName):
    cmd = 'runas /savecred /user:administrator ' + fileName
    os.system(cmd)

if __name__ == "__main__":
    syncRun('C:\Users\sas-shs\Desktop\VP9\PowerTestSuite\TestClient\socWatchBat\soc.bat')