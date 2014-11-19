#coding = utf-8
import socket
from Config import appConfig
import os
from common import syncAdminRun,switchTo1080,switchTo4K,is4kMetric,appendLog,matchCase,parseClipInfo,syncRun
import csv
from App import App
import time
import re
import string
from emon import EmonProcessor

pwd = os.getcwd()
tempFolder = 'localProcess'

def switchDisplay(clipResolution):
    if(clipResolution == "2160" and not is4kMetric()):
        switchTo4K()
    if(clipResolution == "1080" and is4kMetric() ):
        switchTo1080()

def addStartupService():
    command = 'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v Client /t reg_sz /d "%s\\run.bat" /f' % pwd
    os.system(command)

def removeStartupService():
    command = 'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v client /f'
    os.system(command)

def restartOS():
    command = 'shutdown -r -t 0'
    os.system(command)
    time.sleep(10)

def postProcess(clip,frameNum):
    tempDataFolder = os.path.join(tempFolder,clip)
    command = "mkdir %s" % tempDataFolder
    os.system(command)
    appendLog(command)

    binPath = os.path.join(tempDataFolder,clip+".bin")
    command = 'move *.bin ' + binPath
    os.system(command)

    command = 'MVPGTParser.exe ' + binPath
    os.system(command)

    cpuReport = os.path.join(tempDataFolder,clip+"_CPU_Usage.csv")
    command = 'move CPU_Usage.csv ' + cpuReport
    os.system(command)

    fpsReport = os.path.join(tempDataFolder,clip+".txt")
    command = 'move %s.txt %s' %(clip,fpsReport)
    os.system(command)

    socWatchReport = os.path.join(tempDataFolder,clip+".csv")
    command = 'move socRes\%s.csv %s' %(clip,socWatchReport)
    os.system(command)
    
    gpuReport = os.path.join(tempDataFolder,clip+"_GPU_Usage.csv")
    command = 'move Report.csv ' + gpuReport
    os.system(command)

    emonReport = os.path.join(tempDataFolder,clip+"_Emon.csv")
    command = 'move emon.csv ' + emonReport
    os.system(command)

    cpuUsage = getCPUUsage(cpuReport)
    gpuUsage,gpuTime = getGPUUsage(gpuReport)
    fps = getFpsInfo(fpsReport,gpuTime,frameNum)
    getSocRes(socWatchReport,"CPU","GPU","BW")
    pkgPower = '0'
    try:
        myEmonProcessor = EmonProcessor(emonReport)
        emonRes = myEmonProcessor.run()
    except:
        appendLog("emon raw data file no found!")
    finally:
        emonRes = None
    return fps,gpuUsage,cpuUsage,emonRes

def enableChrome():
    MSDKDir = 'C:\Program Files\Intel\Media SDK'
    appendLog("enable chrome...")
    mftDll = os.path.join(MSDKDir,'mfx_mft_vp9vd_32.dll')
    os.system('copy /y chromeDll "%s"' % MSDKDir)
    syncAdminRun('regsvr32 "%s"' % mftDll)
    
def getCPUUsage(cpuReport):
    cpuUsage = "0"
    try:
        reader = csv.reader(file(cpuReport, 'rb'))
        for line in reader:
            if cmp(line[0], "CPU Usage:") == 0:
                cpuUsage = line[1].lstrip()
                cpuUsage = cpuUsage.rstrip('%')
                appendLog(cpuUsage)
    except:
        appendLog("no cpu report file found!...")
    return cpuUsage

def getGPUUsage(gpuReport):
    gpuUsage = "0"
    gpuTime = '0'
    try:
        handle = open(gpuReport,'r')
        contents = handle.read()
        handle.close()
        pos = contents.rindex("Total Time")
        gpuTime = contents[pos+21:pos+29]
        reader = csv.reader(file(gpuReport, 'rb'))
        for line in reader:
            if cmp(line[1], "GPU Utilization(%)") == 0:
                gpuUsage = line[2].rstrip()
                appendLog(gpuUsage)
    except:
        appendLog("no gpu report found!")
    return gpuUsage,gpuTime

def getFpsInfo(fpsReport,gpuTime=None,frameNum=0):
    fps = "0"
    if( os.path.getsize(fpsReport) > 0 ):
        try:
            contents = open(fpsReport,"r").read()
            pos = contents.rindex("fps") - 20
            if("mfx" in contents):
                patten = ".+ (\d+\.\d+) fps"
                fps = matchCase(contents,patten,pos)
                appendLog( "fps : %s" % fps)
            elif("fps" in contents):
                patten = ".+\((\d+\.\d+) fps"
                fps = matchCase(contents,patten,pos)
                appendLog( "fps : %s" % fps)
        except:
            appendLog("App hang or Chrome run, so fps could mot be found in the log..")
    else:
        fps = int(frameNum) / string.atof(gpuTime)
        appendLog( "chrome fps : %s" % fps)
    return fps

def genSocWatchBat(clipName,clipLength):
    Cmd = '%s\\app\socwatch.lnk -t %s --max-detail -f ddr-bw  -f cpu-pstate  -f gfx-pstate -f sys -o %s\socRes\%s' % (pwd,clipLength,pwd,clipName)
    batFileName = '%s\socWatchBat\soc.bat' % pwd
    fileHandle = open(batFileName,'w')
    fileHandle.write(Cmd)
    fileHandle.close()
    return batFileName

def calAveFreq(gpuFreqList):
    temp = 0
    for dataPair in gpuFreqList:
        temp = temp + int(dataPair[0]) * string.atof(dataPair[1])
    aveGpuFreq = temp / 100
    return aveGpuFreq

def getSocRes(socLogFile,*args):
    result = []
    try:
        fileHandle = open(socLogFile,'r')
        content = fileHandle.read()
        fileHandle.close()
    except:
        appendLog("no soc log file found!..")
        return ['0','0','0']
    for opt in args:
        if( opt in "GPU"):
            aveGPUFreq = "0"
            pos = content.index("GT P-State")
            patten = re.compile("\n(\d+)MHz\s+,\s+(\d+\.\d+)%,.*")
            gpuFreqList = patten.findall(content,pos)
            aveGPUFreq = calAveFreq(gpuFreqList)
            appendLog("aveGPUFreq : %s" % aveGPUFreq)
            result.append(aveGPUFreq)
        elif( opt in "CPU"):
            aveCPUFreq = "0"
            pos = content.index("AvgFreq")
            matchedCase = ".*AvgFreq,\s+,\s+(\d+)MHz.*"
            aveCPUFreq = int(matchCase(content,matchedCase,pos))
            appendLog("aveCPUFreq : %s" % aveCPUFreq)
            result.append(aveCPUFreq)
        elif( opt in "BW"):
            memBandwidth = "0"
            pos = content.index("Total Memory Bandwidth")
            matchedCase = ".*=, (\d+\.\d+),\n"
            memBandwidth = string.atof(matchCase(content,matchedCase,pos))
            appendLog("BW : %s" % memBandwidth)
            result.append(memBandwidth)
    return result

class testClient(object):

    def __init__(self,testCfg,appCfgOpt):
        self.myAppCfg = appConfig(appCfgOpt)
        self.appCfgOpt = appCfgOpt
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.testCfg = testCfg
        self.testApp = App(self.myAppCfg)
        self.testApp.genCMDParam()

    def writeRunList(self):
        toRunListHandle = open(self.testCfg.todoList,'w')
        doneListHandle = open(self.testCfg.doneList,'r')
        clips = doneListHandle.read()
        toRunListHandle.write(clips)
        toRunListHandle.close()
        doneListHandle.close()

    def removeDoneCase(self,clipsToRunList,clipNameToRun):
        appendLog("removing the clip : %s" % clipNameToRun )
        for i in range(len(clipsToRunList)):
            case = clipsToRunList[i]
            if( clipNameToRun in case):
                case = "0" + case[1:len(case)]
                clipsToRunList[i] = case
                context = ''.join(clipsToRunList)
                listToRunWriteHandle = open(self.testCfg.todoList,'w')
                listToRunWriteHandle.write(context)
                listToRunWriteHandle.close()
                return

    def getRunCase(self):
        i = 0
        runCase = None
        listToRunReadHandle = open(self.testCfg.todoList,'r')
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

    def runReg(self):
        cmd = "regedit /S %s" % self.myAppCfg.regFile
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
        # self.runReg()
        appendLog("adding the script into OS start up option...")
        addStartupService()
        appendLog("starting the app hang monitor service...")
        syncAdminRun(self.testCfg.hangService.replace("pwd",pwd))
        while True:
            caseToRunList,clipNameToRun = self.getRunCase()
            if( clipNameToRun != None ):
                appendLog("Current case : %s" % clipNameToRun)
                if("end" in clipNameToRun):
                    self.sock.sendto(clipNameToRun,self.testCfg.address)
                    appendLog("%s  power test end..." % clipNameToRun)
                    self.removeDoneCase(caseToRunList,clipNameToRun)
                elif("back" in clipNameToRun):
                    self.sock.sendto(clipNameToRun,self.testCfg.address)
                    time.sleep(180)
                    self.sock.sendto(clipNameToRun, self.testCfg.address)
                    appendLog("%s  power test end..." % clipNameToRun)
                    self.removeDoneCase(caseToRunList,clipNameToRun)
                elif("-" in clipNameToRun):
                    os.system("tool\installDriver.exe %s" % self.myAppCfg.driver)
                    enableChrome()
                    self.removeDoneCase(caseToRunList,clipNameToRun)
                    restartOS()
                else:
                    clipResolution,targetFPS,frameNum,tenBitOpt = parseClipInfo(clipNameToRun)
                    batFileName = self.testApp.genBatFile(clipNameToRun,targetFPS,tenBitOpt,self.appCfgOpt)
                    time.sleep(20)
                    appendLog("switch display monitor...")
                    switchDisplay(clipResolution)
                    clipLength = int(frameNum) / int (targetFPS)
                    appendLog("clip length : %s" % clipLength)
                    time.sleep(15)
                    if(self.testCfg.emon == "True"):
                        syncRun("emon_BDW.bat")
                    if( self.testCfg.MVP == "True"):
                        MVPCmd = "MVP_Agent.exe -t %s" % batFileName
                        self.sock.sendto(clipNameToRun,self.testCfg.address)
                        os.system(MVPCmd)
                        self.sock.sendto(clipNameToRun,self.testCfg.address)                        
                        appendLog("%s  power test end..." % clipNameToRun)                    
                    else:
                        if(self.testCfg.socWatch == "True"):                            
                            appendLog("starting the SocWatch...")					
                            socWatchBat = genSocWatchBat(clipNameToRun,clipLength)
                            syncAdminRun(socWatchBat)
                            time.sleep(5)
                        fps = getFpsInfo(clipNameToRun+".txt")
                        time.sleep(120)
                    fps,gpuUsage,cpuUsage,pkgPower = postProcess(clipNameToRun,frameNum)
                    if( fps != '0' or "Chrome" in self.appCfgOpt):
                        self.removeDoneCase(caseToRunList,clipNameToRun)
                    else:
                        rmBatFileCmd = 'del bat\%s.bat' % batFileName
                        os.system(rmBatFileCmd)
                    if(self.testCfg.restartSvr == "True"):
                        time.sleep(15)
                        restartOS()                        
                    else:
                        time.sleep(60)
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