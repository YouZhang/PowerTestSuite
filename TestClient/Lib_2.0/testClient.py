#coding = utf-8
import socket
from Config import myAppCfg
from common import *
import csv
from App import App
import time

pwd = os.getcwd()
tempFolder = 'localProcess'

def switchDisplay(clipResolution):
    if(clipResolution == "2160" and not is4kMetric()):
        switchTo4K()
    if(clipResolution == "1080" and is4kMetric() ):
        switchTo1080()

def addStartupService():
    command = 'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v Client /t reg_sz /d "%s\PowerTestClient.py" /f' % pwd
    os.system(command)

def removeStartupService():
    command = 'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v client /f'
    os.system(command)

def restartOS():
    command = 'shutdown -r'
    os.system(command)

def postProcess(clip):
    tempMVPFolder = os.path.join(tempFolder,clip)
    command = "mkdir %s" % tempMVPFolder
    os.system(command)
    appendLog(command)

    binPath = os.path.join(tempMVPFolder,clip+".bin")
    command = 'move *.bin ' + binPath
    os.system(command)

    command = 'MVPGTParser.exe ' + binPath
    os.system(command)

    cpuReport = os.path.join(tempMVPFolder,clip+"_CPU_Usage.csv")
    command = 'move CPU_Usage.csv ' + cpuReport
    os.system(command)
	
    fpsReport = os.path.join(tempMVPFolder,clip+".txt")
    command = 'move %s.txt %s' %(clip,fpsReport)
    os.system(command)

    gpuReport = os.path.join(tempMVPFolder,clip+"_GPU_Usage.csv")
    command = 'move Report.csv ' + gpuReport
    os.system(command)
    cpuUsage = getCPUUsage(cpuReport)
    gpuUsage = getGPUUsage(gpuReport)
    fps = getFpsInfo(fpsReport)
    return fps,gpuUsage,cpuUsage

def getCPUUsage(cpuReport):
    cpuUsage = "0"
    reader = csv.reader(file(cpuReport, 'rb'))
    for line in reader:
        if cmp(line[0], "CPU Usage:") == 0:
            cpuUsage = line[1].lstrip()
            cpuUsage = cpuUsage.rstrip('%')
            appendLog(cpuUsage)
    return cpuUsage

def getGPUUsage(gpuReport):
    gpuUsage = "0"
    reader = csv.reader(file(gpuReport, 'rb'))
    for line in reader:
        if cmp(line[1], "GPU Utilization(%)") == 0:
            gpuUsage = line[2].rstrip()
            appendLog(gpuUsage)
    return gpuUsage

def getFpsInfo(fpsReport):
    try:
        contents = open(fpsReport,"r").read()
        pos = contents.rindex("fps") - 20
        if("mfx" in contents):
            patten = ".+ (\d+\.\d+) fps"
            fps = matchCase(contents,patten,pos)
            appendLog( "fps : %s" % fps)
        else:
            patten = ".+\((\d+\.\d+) fps"
            fps = matchCase(contents,patten,pos)
            appendLog( "fps : %s" % fps)
    except:
        appendLog("App hang and fps could mot be found in the log..")
        fps = None
    return fps

class testClient(object):

    def __init__(self,testCfg):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.testCfg = testCfg
        self.testApp = App(myAppCfg)
        self.testApp.genCMDParam()

    def writeRunList(self):
        toRunListHandle = open(self.testCfg.todoList,'w')
        doneListHandle = open(self.testCfg.doneList,'r')
        clips = doneListHandle.read()
        toRunListHandle.write(clips)
        toRunListHandle.close()
        doneListHandle.close()

    def removeDoneCase(self,clipsToRunList):
        context = ''.join(clipsToRunList[1:len(clipsToRunList)])
        listToRunWriteHandle = open(self.testCfg.todoList,'w')
        listToRunWriteHandle.write(context)
        listToRunWriteHandle.close()

    def getRunCase(self):
        i = 0
        runCase = None
        listToRunReadHandle = open(self.testCfg.todoList,'r')
        caseToRunList = listToRunReadHandle.readlines()
        listToRunReadHandle.close()
        try:
            state,case = caseToRunList[0].split()
        except:
            appendLog("empty list ...")
            return None

        while True:
            if( state == "1"):
                runCase = case
                break
            i += 1
            state,case = caseToRunList[i].split()
        return caseToRunList,runCase

    def runReg(self):
        cmd = "regedit /S %s" % myAppCfg.regFile
        os.system(cmd)

    def setPowerConfig(self):
        myPowerConfig = self.testCfg.powerConfig
        cmd = 'powercfg -l > powerConfig.txt'
        os.system(cmd)
        fileHandle = open("powerConfig.txt","r")
        lines = fileHandle.readlines()
        guid = None
        for line in lines:
            if (myPowerConfig in line):
                guid = line[19:55]
                break
        setPowerCfgCmd = 'powercfg /s %s' % guid
        appendLog("Current power config : %s mode" % myPowerConfig)
        os.system(setPowerCfgCmd)

    def run(self):
        self.setPowerConfig()
        self.runReg()
        appendLog("adding the script into OS start up option...")
        addStartupService()
        appendLog("starting the app hang monitor service...")
        syncRun(self.testCfg.hangService.replace("pwd",pwd))
        while True:
            caseToRunList,clipNameToRun = self.getRunCase()
            if( caseToRunList ):
                appendLog("Current test clip : %s" % clipNameToRun)
                if("end" in clipNameToRun):
                    self.sock.sendto(clipNameToRun,self.testCfg.address)
                    appendLog("%s  power test end..." % clipNameToRun)
                    self.removeDoneCase(caseToRunList)
                elif("back" in clipNameToRun):
                    self.sock.sendto(clipNameToRun,self.testCfg.address)
                    time.sleep(180)
                    self.sock.sendto(clipNameToRun, self.testCfg.address)
                    appendLog("%s  power test end..." % clipNameToRun)
                    self.removeDoneCase(caseToRunList)
                else:
                    clipResolution,targetFPS,frameNum,tenBitOpt = parseClipInfo(clipNameToRun)
                    batFileName = self.testApp.genBatFile(clipNameToRun,targetFPS,tenBitOpt,"fixedPlayback")
                    switchDisplay(clipResolution)
                    clipLength = int(frameNum) / int (targetFPS)
                    appendLog("clip length : %s" % clipLength)
                    time.sleep(40)
                    if( self.testCfg.MVP == "True"):
                        MVPCmd = "MVP_Agent.exe -t %s" % batFileName
                        self.sock.sendto(clipNameToRun,self.testCfg.address)
                        os.system(MVPCmd)
                        self.sock.sendto(clipNameToRun,self.testCfg.address)
                        appendLog("%s  power test end..." % clipNameToRun)
                    else:
                        os.system(batFileName)
                    fps,gpuUsage,cpuUsage = postProcess(clipNameToRun)
                    if( fps != None):
                        self.removeDoneCase(caseToRunList)
                        restartOS()
                appendLog("-------------------------------------------------")
            else:
                self.writeRunList()
                self.sock.sendto("done",self.testCfg.address)
                appendLog( "all clips power test done!\nremoving startup service...")
                appendLog("Power test finished...")
                self.sock.close()
                removeStartupService()
                os.system("localCalculate.py")
                break