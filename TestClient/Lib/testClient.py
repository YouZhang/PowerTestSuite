#coding = utf-8
import socket
from Config import myAppCfg
from common import *
import csv
from App import App
import time
from Diagram import diagram

def switchDisplay(clipResolution):
    if(clipResolution == "2160" and not is4kMetric()):
        switchTo4K()
    if(clipResolution == "1080" and is4kMetric() ):
        switchTo1080()


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

    gpuReport = clip + '\\' + clip + '_Report.csv'
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

    fps = "0"
    fpsReport = clip + '.txt'
    logFp = file(fpsReport)
    contents = logFp.read()
    posStart = contents.rindex("(")
    posEnd = contents.rindex("fps")
    fps = contents[posStart+1:posEnd -1]
    appendLog( "fps : %s" % fps)


class testClient(object):

    def __init__(self,testCfg):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.testCfg = testCfg
        self.testApp = App(myAppCfg)
        self.testApp.genCMDParam()

    def wirteRunList(self):
        toRunListHandle = open(self.testCfg.doneList,'w')
        doneListHandle = open(self.testCfg.todoList,'r')
        clips = doneListHandle.read()
        toRunListHandle.write(clips)
        toRunListHandle.close()
        doneListHandle.close()

    def removeDoneCase(self,clipsToRunList):
        context = ''.join(clipsToRunList[1:len(clipsToRunList)])
        listToRunWriteHandle = open(self.testCfg.todoList,'w')
        listToRunWriteHandle.write(context)
        listToRunWriteHandle.close()

    def readRunList(self):
        listToRunReadHandle = open(self.testCfg.todoList,'r')
        clipsToRunList = listToRunReadHandle.readlines()
        listToRunReadHandle.close()
        return clipsToRunList

    def runReg(self):
        cmd = "regedit %s" % self.testCfg.regFile
        os.system(cmd)

    def run(self):
        while True:
            clipsToRunList = self.readRunList()
            if( clipsToRunList != [] ):
                clipNameToRun = clipsToRunList[0].strip('\n')
                appendLog("Current test clip : %s" % clipNameToRun)
                if("end" in clipNameToRun):
                    self.sock.sendto(clipNameToRun,self.testCfg.address)
                    appendLog("%s  power test end..." % clipNameToRun)
                    self.removeDoneCase(clipsToRunList)
                elif("back" in clipNameToRun):
                    self.sock.sendto(clipNameToRun,self.testCfg.address)
                    time.sleep(180)
                    self.sock.sendto(clipNameToRun, self.testCfg.address)
                    appendLog("%s  power test end..." % clipNameToRun)
                    self.removeDoneCase(clipsToRunList)
                else:
                    clipResolution,targetFPS,frameNum,batFileName = self.testApp.genBatFile(clipNameToRun,"fixedPlayback")
                    switchDisplay(clipResolution)
                    clipLength = int(frameNum) / int (targetFPS)
                    MVPCmd = "MVP_Agent.exe -t " + batFileName
                    self.sock.sendto(clipNameToRun,self.testCfg.address)
                    os.system(MVPCmd)
                    self.sock.sendto(clipNameToRun,self.testCfg.address)
                    appendLog("%s  power test end..." % clipNameToRun)
                    self.removeDoneCase(clipsToRunList)
                    postProcess(clipNameToRun)
                    time.sleep(75)
                    appendLog("will sleep 75s....")
                appendLog("-------------------------------------------------")
            else:
                self.wirteRunList()
                self.sock.sendto("done",self.testCfg.address)
                appendLog( "all clips power test done!\nremoving startup service...")
                appendLog("Power test finished...")
                self.sock.close()
                break



