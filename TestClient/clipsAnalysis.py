#coding = utf-8
import sys
sys.path.append("Lib_2.0")
from common import appendLog,cmdRun,syncRun,getFileSize,getDir,parseClipInfo,move
import time
from threading import Thread
import glob


def analysisClips(clipName):
    clipInfoFile = "clipInfo.txt"
    cmd = "tool\\ClipsAnalysis.exe -regress Clips\%s > %s.info" % (clipName,clipName)
    cmdRun(cmd)

def killSrv():
    time.sleep(6.5)
    killSrv = "taskkill -f -im java*"
    cmdRun(killSrv)

def getCLipInfo(clipName):
    with open(clipName+".info",'r') as file:
        for line in file:
            if("pictures" in  line):
                pos = line.index("pictures")
                frameNum = line[0:pos-1]
                resolution = line[pos+10:len(line)-1]
                resolution = resolutionChange(resolution)
                appendLog("frame num : %s " % frameNum)
                appendLog("resolution : %s " % resolution)
                return frameNum,resolution

def resolutionChange(resolution):
    if("3840" in resolution):
        return "2160"
    elif("1080" in resolution):
        return "1080"
    elif("720" in resolution):
        return "720"


def launch(clipName):
    resolution,targetFPS,frameNum,tenBit = parseClipInfo(clipName)
    name = clipName[0:5]
    if(resolution == -1 or frameNum == -1):
        threadList = []
        analysisThread = Thread(target=analysisClips,args=(clipName,))
        threadList.append(analysisThread)
        getInfoThread = Thread(target=killSrv,args=())
        threadList.append(getInfoThread)
        for t in threadList:
            t.setDaemon(True)
            t.start()
        t.join()
        frameNum_,resolution_ = getCLipInfo(clipName)
        try:
            totalTime = int(frameNum_) / int(targetFPS)
            bitRate = int(getFileSize("Clips\\"+clipName) / 1024 * 8.127 / totalTime)
        except ZeroDivisionError:
            exit(-1)
        newClipName = "%s_%sfps_%skbps_%sframe_%sp_m8.webm" % (name,targetFPS,bitRate,frameNum_,resolution_)
        newClipPath = getDir(folder,newClipName)
        move(clipPath,newClipPath)
        appendLog("newClipName : %s" % newClipName)
    else:
        appendLog("clip name matched..")

def getClipsList(folderName):
    patten = getDir(folderName,"*.webm")
    vp9ClipsList = glob.glob(patten)
    return vp9ClipsList

if __name__ == "__main__":
    global folder
    folder = sys.argv[1]
    vp9ClipsList = getClipsList(folder)
    for clipPath in vp9ClipsList:
        clipName = clipPath.split("\\")[1]
        launch(clipName)
        appendLog("------------------------------------------------")
    appendLog("finished")






