#coding = utf-8
import socket
import sys
import os
import time
sys.path.append("Lib_1.0")
from common import appendLog
from App import *
from multiprocessing import Process,Pipe
import csv
import Diagram

runList = os.path.join("RunList","list_ToRun.txt")
doneList = os.path.join("RunList","list_done.txt")
address = ('10.239.140.232', 31500)
# address = ('127.0.0.1', 31500)
testAppName = "mv_decoder_adv"
parentConn,childConn = Pipe()
global clipNameToRun
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def addStartupService():
    command = 'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v Client /t reg_sz /d "F:\SHU\PowerTestSuite\TestClient\client.py" /f'
    os.system(command)

def removeStartupService():
    command = 'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v client /f'
    os.system(command)

def restartOS():
    command = 'shutdown -r'
    os.system(command)

def writeClips(fromFile,toFile):
    toRunListHandle = open(toFile,'w')
    doneListHandle = open(fromFile,'r')
    clips = doneListHandle.read()
    toRunListHandle.write(clips)
    toRunListHandle.close()
    doneListHandle.close()

def runMVPCmd(batFileName,clipNameToRun,conn):
    sock.sendto(clipNameToRun, address)
    os.system(batFileName)
    sock.sendto(clipNameToRun,address)
    postProcess(clipNameToRun)
    conn.send("done")


def postProcess(clip):
    command = 'mkdir ' + clip
    os.system(command)
    appendLog(command)

    binPath = clip + '\\' + clip + '.bin'
    command = 'move *.bin ' + binPath
    os.system(command)

    command = 'MVPGTParser.exe ' + binPath
    os.system(command)

    cpuReport = clip + '\\' + clip + '_CPU_Usage.csv'
    command = 'move CPU_Usage.csv ' + cpuReport
    os.system(command)

    gpuReport = clip + '\\' + clip + 'GPU_Report.csv'
    command = 'move Report.csv ' + gpuReport
    os.system(command)
    cpuUsage = "0"
    reader = csv.reader(file(cpuReport, 'rb'))
    for line in reader:
        if cmp(line[0], "CPU Usage:") == 0:
            cpuUsage = line[1].lstrip()
            cpuUsage = cpuUsage.rstrip('%')
            appendLog(cpuUsage)
    gpuUsage = "0"
    reader = csv.reader(file(gpuReport, 'rb'))
    for line in reader:
        if cmp(line[1], "GPU Utilization(%)") == 0:
            gpuUsage = line[2].rstrip()
            appendLog(gpuUsage)

    fpsReport = clip + '.txt'

    try:
        logFp = file(fpsReport)
        contents = logFp.read()
        endPos = contents.rindex("fps")
        fps = contents[endPos-8:endPos-1]
        endPos = contents.rindex("CPU usage")
        cpuUsage = contents[32:40]
        # posStart = contents.rindex("(")
        # posEnd = contents.rindex("fps")
        # fps = contents[posStart+1:posEnd -1]

        appendLog( "fps : %s" % fps)
    except:
        appendLog("App hang and fps could mot be found in the log..")
        fps = "XXXX"
    return fps,gpuUsage,cpuUsage

def runSocWatchBat(batFileName,conn):
    cmd = "cmd /c start %s" % batFileName
    os.system(cmd)


def initEnv():
    cleanCMD = "del *.bin"
    os.system(cleanCMD)

initRow = ("Cases","CPU","GPU","FPS")
resultFile = common.localTime + ".xlsx"
myDiagram = Diagram.diagram(resultFile,initRow)

if __name__ == "__main__":

    initEnv()

    while True:

        addStartupService()
        listToRunReadHandle = open('RunList\List_ToRun.txt','r')
        clipsToRunList = listToRunReadHandle.readlines()
        listToRunReadHandle.close()

        if( clipsToRunList != [] ):
            clipNameToRun = clipsToRunList[0].strip('\n')

            appendLog("Current test clip : %s" % clipNameToRun)
            if("end" in clipNameToRun):
                sock.sendto(clipNameToRun, address)
                appendLog("%s  power test end..." % clipNameToRun)
                context = ''.join(clipsToRunList[1:len(clipsToRunList)])
                listToRunWriteHandle = open('RunList\List_ToRun.txt','w')
                listToRunWriteHandle.write(context)
                listToRunWriteHandle.close()
            # appProcess(testAppName,clipNameToRun)
            elif("back" in clipNameToRun):
                sock.sendto(clipNameToRun, address)
                time.sleep(180)
                sock.sendto(clipNameToRun, address)
                appendLog("%s  power test end..." % clipNameToRun)
                context = ''.join(clipsToRunList[1:len(clipsToRunList)])
                listToRunWriteHandle = open('RunList\List_ToRun.txt','w')
                listToRunWriteHandle.write(context)
                listToRunWriteHandle.close()
            else:
                clipResolution,targetFPS,frameNum = common.parseClipInfo(clipNameToRun)
                if(clipResolution == "2160" and not common.is4kMetric()):
                    common.switchTo4K()
                if(clipResolution == "1080" and common.is4kMetric() ):
                    common.switchTo1080()

                clipLength = int(frameNum) / int (targetFPS)
                batFileName =  clipNameToRun + '.bat'
                MVPCmd = "MVP_Agent.exe -t " + batFileName
                sock.sendto(clipNameToRun, address)
                os.system(MVPCmd)
                sock.sendto(clipNameToRun,address)
                fps,gpuUsage,cpuUsage = postProcess(clipNameToRun)

                # mvpData = (clipNameToRun,cpuUsage,gpuUsage,fps)
                # myDiagram.addData(mvpData)
                # socWatchCMD = 'app\socwatch.lnk -t %s --max-detail -f ddr-bw  -f cpu-cstate -f cpu-pstate -f gfx-cstate -f gfx-pstate  -f sys  -f energy -o C:\Users\sas-shs\Desktop\VP9\PowerTestSuite\TestClient\%s' % (clipLength,clipNameToRun)
                # appendLog(socWatchCMD)
                # socWatchBat = "socWatch_" + clipNameToRun + '.bat'
                
                # socWatchProc = Process(target=runSocWatchBat,args=(socWatchCMD,childConn))
                # socWatchProc.start()
                #####################
                # MVPProc = Process(target=runMVPCmd,args=(MVPCmd,clipNameToRun,childConn))
                # MVPProc.start()
                # while True:
                #     if(parentConn.recv() == "done"):
                #         break
                appendLog("%s  power test end..." % clipNameToRun)				
                context = ''.join(clipsToRunList[1:len(clipsToRunList)])
                listToRunWriteHandle = open('RunList\List_ToRun.txt','w')
                listToRunWriteHandle.write(context)
                listToRunWriteHandle.close()                
                time.sleep(180)
                appendLog("will sleep 70s....")
            appendLog("-------------------------------------------------")

            # restartOS()
        else:
            writeClips(doneList,runList)
            sock.sendto("done",address)
            appendLog( "all clips power test done!\nremoving startup service...")
            # myDiagram.genDiagram()
            # removeStartupService()
            appendLog("Power test finished...")
            sock.close()
            break