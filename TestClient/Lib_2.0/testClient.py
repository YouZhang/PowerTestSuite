#coding = utf-8
import socket
from Config import appConfig
from common import *
import csv
from App import App
import time
import re
import string
from emon import EmonProcessor

##TODO:specific the OS
def addStartupService():
    appendLog("adding the script into OS start up option...")
    command = 'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v Client /t reg_sz /d "%s\\run.bat" /f' % pwd
    cmdRun(command)

def removeStartupService():
    command = 'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v client /f'
    cmdRun(command)

def restartOS():
    time.sleep(2)
    command = 'shutdown -r -t 0'
    cmdRun(command)
    time.sleep(10)

def enableChrome():
    MSDKDir = '\'C:\\Program Files\\Intel\\Media SDK\''
    appendLog("enable chrome...")
    copy("chromeDll",MSDKDir)
    mftDll = getDir(MSDKDir,'mfx_mft_vp9vd_32.dll')
    syncAdminRun('regsvr32 "%s"' % mftDll)
    
def getCPUUsage(cpuReport):
    cpuUsage = "0"
    try:
        reader = csv.reader(file(cpuReport, 'rb'))
        for line in reader:
            if cmp(line[0], "CPU Usage:") == 0:
                cpuUsage = line[1].lstrip()
                cpuUsage = cpuUsage.rstrip('%')
                appendLog("CPU Utilization : " + cpuUsage)
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
                appendLog("GPU Utilization : " + gpuUsage)
    except:
        appendLog("no gpu report found!")
    return gpuUsage,gpuTime

def getFpsInfo(fpsReport,gpuTime=None,frameNum=0):
    fps = "0"
    if( os.path.getsize(fpsReport) > 0 ):
        try:
            contents = open(fpsReport,"r").read()
            pos = contents.rindex("fps") - 10
            if("mfx" in contents):
                patten = ".+ (\d+\.\d+) fps"
                fps = matchCase(contents,patten,pos)
                appendLog( "fps : %s" % fps)
            elif("ffplay" in contents):
                fps = int(frameNum) / string.atof(gpuTime)
                appendLog( "fps : %s" % fps)
            elif("ffmpeg" in contents):
                patten = ".+fps= (\d+) .+"
                fps = matchCase(contents,patten,pos)
                appendLog( "fps : %s" % fps)
            elif("fps" in contents):
                patten = ".+\((\d+\.\d+) fps"
                fps = matchCase(contents,patten,pos)
                appendLog( "fps : %s" % fps)

        except:
            appendLog("App hang or Chrome run, so fps could mot be found in the log..")
    else:
        try:
            fps = int(frameNum) / string.atof(gpuTime)
            appendLog( "chrome fps : %s" % fps)
        except ZeroDivisionError:
            appendLog("gpuTime = 0...")
    return fps

def genSocWatchBat(clipName,clipLength):
    cmd = '%s\\tool\socwatch.lnk -t %s --max-detail -f ddr-bw  -f cpu-pstate  -f gfx-pstate -f sys -o "%s\socRes\%s"' % (pwd,clipLength,pwd,clipName)
    batFileName = '%s\socWatchBat\soc.bat' % pwd
    fileHandle = open(batFileName,'w')
    fileHandle.write(cmd)
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
            try:
                pos = content.index("GT P-State")
                patten = re.compile("\n(\d+)MHz\s+,\s+(\d+\.\d+)%,.*")
                gpuFreqList = patten.findall(content,pos)
                aveGPUFreq = calAveFreq(gpuFreqList)
                appendLog("aveGPUFreq : %s" % aveGPUFreq)
                result.append(aveGPUFreq)
            except:
                result.append("Error")
        elif( opt in "CPU"):
            try:
                pos = content.index("AvgFreq")
                matchedCase = ".*AvgFreq,\s+,\s+(\d+)MHz.*"
                aveCPUFreq = int(matchCase(content,matchedCase,pos))
                appendLog("aveCPUFreq : %s" % aveCPUFreq)
                result.append(aveCPUFreq)
            except:
                result.append("Error")
        elif( opt in "BW"):
            try:
                pos = content.index("Total Memory Bandwidth")
                matchedCase = ".*=, (\d+\.\d+),\n"
                memBandwidth = string.atof(matchCase(content,matchedCase,pos))
                appendLog("BW : %s" % memBandwidth)
                result.append(memBandwidth)
            except:
                result.append("Error")
    return result

def switchDisplay(clipResolution):
    switchCmd = "tool\switchDisplay.exe " +  clipResolution
    syncRun(switchCmd)

class testClient(object):

    def __init__(self,testCfg,appCfgOpt):
        self.myAppCfg = appConfig(appCfgOpt)
        self.appCfgOpt = appCfgOpt
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.testCfg = testCfg
        self.testApp = App(self.myAppCfg,self.testCfg)
        self.testApp.genCMDParam()

    def runCase(self,clipNameToRun,clipLength):
        appendLog("%s case start..." % clipNameToRun)
        batFileName = getDir(self.testCfg.batFilePath,clipNameToRun + '.bat')
        if(self.testCfg.MVP == "True"):
            command = "MVP_Agent.exe -t %s" % batFileName
        else:
            command = batFileName
        if(self.testCfg.emon == "True"):
            syncRun("emon.bat")
        if( self.testCfg.powerMeasure == "True"):
            try:
                self.sock.sendto(clipNameToRun,self.myAppCfg.address)
                cmdRun(command)
                self.sock.sendto(clipNameToRun,self.myAppCfg.address)
            except:
                appendLog("Please check the network...")
                exit(-1)
        else:
            if(self.testCfg.socWatch == "True"):
                appendLog("starting the SocWatch...")
                cmd = genSocWatchBat(clipNameToRun,clipLength)
                syncAdminRun(cmd)
                time.sleep(5)
                cmdRun(command)
                cmdRun("taskkill /f /im emon*")
                #left some time to generate the final soc report
                while( True ):
                    time.sleep(5)
                    if( checkProcStatus("socwatch") == 0):
                        break
            else:
                cmdRun(command)
        cmdRun("taskkill /f /im emon*")
        appendLog("%s case end..." % clipNameToRun)

    def postProcess(self,clip,frameNum):
        tempDataFolder = os.path.join(self.testCfg.tempFolder,clip)
        mkdir(tempDataFolder)

        binFile = getDir(tempDataFolder,clip + ".bin")
        move("*.bin",binFile)

        command = 'MVPGTParser.exe "%s"' % binFile
        cmdRun(command)

        cpuReport = getDir(tempDataFolder,clip+"_CPU_Usage.csv")
        move("CPU_Usage.csv",cpuReport)

        fpsReport = getDir(tempDataFolder,clip+".txt")
        move(clip + ".txt",fpsReport)

        socWatchReport = getDir(tempDataFolder,clip+".csv")
        move("socRes\%s.csv" % clip,socWatchReport)

        gpuReport = getDir(tempDataFolder,clip+"_GPU_Usage.csv")
        move("Report.csv",gpuReport)

        emonReport = getDir(tempDataFolder,clip+"_Emon.csv")
        move("emon.csv",emonReport)

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

    def runReg(self):
        cmd = "regedit /S %s" % self.myAppCfg.regFile
        cmdRun(cmd)

    def setPowerConfig(self):
        myPowerConfig = self.testCfg.powerConfig
        cmd = 'powercfg -l > powerConfig.txt'
        cmdRun(cmd)
        fileHandle = open("powerConfig.txt","r")
        lines = fileHandle.readlines()
        guid = None
        for line in lines:
            if (myPowerConfig in line):
                guid = line[19:55]
                break
        setPowerCfgCmd = 'powercfg /s %s' % guid
        appendLog("Current power config : %s mode" % myPowerConfig)
        cmdRun(setPowerCfgCmd)
    
    def overrideTestConfig(self,paramList):
        for param in paramList:
            paramLow = param.lower()
            if( "sleep" in paramLow):
                self.testCfg.sleepTime = int(param.split()[-1])
            if( "driver" in paramLow):
                self.myAppCfg.driver = param.split()[-1]
            if( "application" in paramLow ):
                self.myAppCfg.appBinary = param.split()[-1] + ' '
            if( "restart" in paramLow ):
                self.myAppCfg.restartSvr = True
            if( "codec" in paramLow):
                self.myAppCfg.param["decoder"] = param.split()[-1]
            if( "runlist" in paramLow):
                self.myAppCfg.runList ="RunList\\" + param.split()[-1]
            if( "emon" in paramLow and "1" in paramLow ):
                self.testCfg.emon = "True"
            if( "socwatch" in paramLow and "1" in paramLow):
                self.testCfg.socWatch = "True"
            if( "mvp" in paramLow and "1" in paramLow):
                self.testCfg.MVP = "True"
            if( "power" in paramLow and "1" in paramLow):
                self.testCfg.powerMeasure = "True"
        
    def run(self):
        appendLog("---------------------------start initail config---------------------------")
        self.setPowerConfig()
        # self.runReg()
        addStartupService()
        if( self.testCfg.hangService == "True"):
            appendLog("starting the app hang monitor service...")
            syncAdminRun("pwd\\Lib_2.0\\appHangMonitor.bat".replace("pwd",pwd))
        appendLog("---------------------------end inital config---------------------------")
        while True:
            if( self.testCfg.driver != ''):
                appendLog("%s will be installed" % self.testCfg.driver)
                cmdRun("tool\installDriver.exe %s" % self.testCfg.driver)
                # enableChrome()
                restartOS()
            caseToRunList,caseToRun,driver,paramList = getRunCase(self.myAppCfg.runList)
            self.overrideTestConfig(paramList)
            if( caseToRun != None ):
                appendLog("Current case : %s" % caseToRun)
                if("end" in caseToRun):
                    self.sock.sendto(caseToRun,self.myAppCfg.address)
                    appendLog("%s end..." % caseToRun)
                    removeDoneCase(self.myAppCfg.runList,caseToRunList,caseToRun)
                    restartOS()
                elif("back" in caseToRun):
                    self.sock.sendto(caseToRun,self.myAppCfg.address)
                    time.sleep(180)
                    self.sock.sendto(caseToRun, self.myAppCfg.address)
                    appendLog("%s  power test end..." % caseToRun)
                    removeDoneCase(self.myAppCfg.runList,caseToRunList,caseToRun)
                else:
                    clipResolution,targetFPS,frameNum,tenBitOpt,clipLength = parseClipInfo(caseToRun)
                    self.testApp.genBatFile(caseToRun,targetFPS,tenBitOpt,self.appCfgOpt)
                    if( "decode" not in self.appCfgOpt.lower() ):
                        appendLog("switch display monitor...")
                        switchDisplay(clipResolution)
                    appendLog("clip length : %s" % clipLength)
                    appendLog("will sleep %s" % self.testCfg.sleepTime)
                    time.sleep(self.testCfg.sleepTime)                    
                    self.runCase(caseToRun,clipLength)
                    fps,gpuUsage,cpuUsage,pkgPower = self.postProcess(caseToRun,frameNum)
                    if( fps != '0'):
                        removeDoneCase(self.myAppCfg.runList,caseToRunList,caseToRun)
                    if(self.testCfg.restartSvr == "True"):
                        time.sleep(self.testCfg.sleepTime)
                        restartOS()                        
                    else:
                        time.sleep(self.testCfg.sleepTime)
                appendLog("-------------------------------------------------")
            else:
                appendLog( "all cases done!...")
                appendLog("finished...")
                self.sock.close()
                # removeStartupService()
                cmdRun("localCalculate.exe %s" % self.appCfgOpt)
                backupData(src="localProcess",mode=self.appCfgOpt)
                break