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
    appendLog('running command : %s' % cmd)
    os.system("%s" % cmd)

def mkdir(path):
    appendLog("make directory %s" % path)
    try:
        cmd = 'mkdir "%s"' % path
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
    cmdRun('del "%s"' % targetFiles)

def copy(src,target):
    appendLog("copy /y files from : %s to %s" % (src,target))
    cmdRun("copy %s %s" % (src,target))

def move(src,target):
    appendLog("move files from %s to %s" % (src,target))
    cmdRun('move "%s" "%s"' % (src,target))

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
    resolution,targetFPS,frameNum = parseClipName(clip)
    tenBit = '8'
    clipLength = None
    command = 'tool\MediaInfo_x86\MediaInfo.exe -f "clips\\%s*"' % clip
    keyWords = ['Bit rate','Width','Bit Depth','Frame rate','Duration','Frame count']
    info = {}
    info['Frame count'] = frameNum
    clipInfoList = os.popen(command).readlines()
    for clipInfo in clipInfoList:
        for keyWord in keyWords:
            clipInfo = clipInfo.replace(" ","")
            patten1 = r"%s:(\d*).*\n" % keyWord.replace(" ","")
            patten2 = r"%s:(\d*\.\d+).*\n" % keyWord.replace(" ","")
            val1 = matchCase(clipInfo,patten1,0)
            val2 = matchCase(clipInfo,patten2,0)
            if( val1 and val2 ):
                value = val2
            elif( val1 is not None):
                value = val1
            else:
                continue
            if(info.has_key(keyWord) ):
                if( len(value) > len(info[keyWord]) ):
                    info[keyWord] = value
            else:
                info[keyWord] = value
    if( info.has_key('Width')):
        if( int(info['Width']) >= 3840):
            resolution = "2160"
        else:
            resolution = "1080"
    if( info.has_key('Bit Depth')):
        tenBit = '10'
    if( info.has_key('Frame rate')):
        targetFPS = int(round(float(info['Frame rate'])))
    if( info.has_key('Duration')):
        clipLength = int(info['Duration']) / 1000
    if( info.has_key('Frame count')):
        frameNum = info['Frame count']
    if( clipLength == None ):
        clipLength = int(frameNum) / int (targetFPS)
    for key in info:
        appendLog("%s : %s" % (key,info[key]))

    return resolution,targetFPS,frameNum,tenBit,clipLength

def parseClipName(clip):
    resMatchedCase = ".*_(\d+)p.*"
    fpsMatchedCase = ".*_(\d+)fps.*"
    frameMatchedCase = ".+_(\d+)frame.+"
    resolution = matchCase(clip,resMatchedCase)
    targetFPS = matchCase(clip,fpsMatchedCase)
    frameNum = matchCase(clip,frameMatchedCase)
    return resolution,targetFPS,frameNum

def matchCase(content,patten,pos=0):
    patten = re.compile(patten)
    matchedItem = patten.match(content,pos)
    if( matchedItem ):
        return matchedItem.group(1)
    else:
        return None

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
        paramList = []
        driver = ""
        listToRunReadHandle = open(runList,'r')
        caseToRunList = listToRunReadHandle.readlines()
        listToRunReadHandle.close()
        while(i < len(caseToRunList)):
            try:
                testCase = caseToRunList[i].split('\t')
                state = testCase[0]
                case = testCase[1]
                if( state == "1"):
                    runCase = case
                    try:
                        paramList = testCase[2:len(testCase)]
                        for param in paramList:
                            if( "Driver" in param ):
                                driver = param.split("*")[-1].strip()
                                testCase.pop()
                                caseToRunList[i] = "\t".join(testCase) + '\n'
                                context = ''.join(caseToRunList)
                                listToRunWriteHandle = open(runList,'w')
                                listToRunWriteHandle.write(context)
                                listToRunWriteHandle.close()
                    except:
                        appendLog(" no additional parameter found...")
                    break
                i += 1
            except:
                appendLog("empty testModelist ...")
                exit(-1)
        return caseToRunList,runCase,driver,paramList

def removeDoneCase(testModeList,caseToRunList,toRemoveCase):
    appendLog("removing the case : %s" % toRemoveCase )
    for i in range(len(caseToRunList)):
        case = caseToRunList[i]
        if( toRemoveCase in case and '1' in case ):
            case = "0" + case[1:len(case)]
            caseToRunList[i] = case
            context = ''.join(caseToRunList)
            listToRunWriteHandle = open(testModeList,'w')
            listToRunWriteHandle.write(context)
            listToRunWriteHandle.close()
            return

def getFileSize(fileName):
    size = os.path.getsize(fileName)
    return size
            
def checkProcStatus(procName):
    cmd = "tasklist | findstr %s" % procName
    ret = os.popen(cmd).readline()
    if( ret != '' ):
        return 1
    else:
        return 0
            
if __name__ == "__main__":
    print checkProcStatus("chrome")
    parseClipInfo('big_60fps_5000kbps_2397frame_1080p_m8')
    # getDir("C:\Users\You\Documents\GitHub\PowerTestSuite\TestClient","a","b")
    # backupData("localProcess","Vp")
    # removeFiles("*.xlsx","..")
    # copy("..\mvp","..")
    # move("..\mvp","..")