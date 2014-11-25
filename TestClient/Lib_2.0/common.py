#coding = utf-8
import os
import re
import win32api
import win32con
import time
from KeyValue import VK_CODE

localTime = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())
pwd = os.getcwd()

def cmdRun(cmd):
    appendLog("running command : %s" % cmd)
    os.system(cmd)

def mkdir(path):
    appendLog("make directory %s" % path)
    try:
        cmd = "mkdir %s" % path
        cmdRun(cmd)
    except WindowsError:
        appendLog("%s already exited..." % path)

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

def appendLog(message,folder="Log"):
    print message
    logfile = getDir(folder,localTime+".log")
    logHandle = open(logfile,"a")
    logHandle.write(str(message) + "\n\n")
    logHandle.close()

def backupData(src,mode):
    """

    :rtype : object
    """
    backFolder = getDir("backup",mode,localTime)
    mkdir(backFolder)
    move(src,target=backFolder)

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
    cmdRun(cmd)

def syncAdminRun(fileName):
    cmd = 'runas /savecred /user:administrator ' + fileName
    cmdRun(cmd)

def getIp(machineName):
    resultFile = "pingRes.txt"
    cmdRun("ping %s > %s" % (machineName,resultFile))
    handle = open(resultFile,'r')
    line = handle.readline()
    if(line == '\n'):
        line = handle.readline()
        try:
            startPos = line.index('[')
            endPos = line.index(']')
            ip = line[startPos+1:endPos]
            appendLog("server ip : %s" % ip)
            if(len(ip) < 10):
                appendLog("cannot find your ip")
                return -1
            return ip
        except:
            appendLog("could not find the server ip, pls check the network config")
            return -1


def getRunCase(runList):
        i = 0
        runCase = None
        listToRunReadHandle = open(runList,'r')
        caseToRunList = listToRunReadHandle.readlines()
        listToRunReadHandle.close()
        while(i < len(caseToRunList)):
            try:
                state,case = caseToRunList[i].split()
                if( state == "1"):
                    runCase = case
                    break
                i += 1
            except:
                appendLog("empty list ...")
                return None,None
        return caseToRunList,runCase

def removeDoneCase(testModeList,caseToRunList,toRemoveCase):
    appendLog("removing the case : %s" % toRemoveCase )
    for i in range(len(caseToRunList)):
        case = caseToRunList[i]
        if( toRemoveCase in case):
            case = "0" + case[1:len(case)]
            caseToRunList[i] = case
            context = ''.join(caseToRunList)
            listToRunWriteHandle = open(testModeList,'w')
            listToRunWriteHandle.write(context)
            listToRunWriteHandle.close()
            return

if __name__ == "__main__":
    getDir("C:\Users\You\Documents\GitHub\PowerTestSuite\TestClient","a","b")
    backupData("localProcess","Vp")
    # removeFiles("*.xlsx","..")
    # copy("..\mvp","..")
    # move("..\mvp","..")