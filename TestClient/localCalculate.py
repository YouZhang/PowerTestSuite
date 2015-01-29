import sys
sys.path.append("Lib_2.0")
from testClient import testClient,getFpsInfo,getGPUUsage,getCPUUsage,getSocRes,getChromeFPS
from Config import testConfig
import os
import string
from Diagram import diagram
from common import *
from emon import EmonProcessor
from emailOperation import *
from SystemInfo import *

try:
    mode = sys.argv[1]
except:
    mode = "tempMode"
    
initRow = ("Cases","CPU(%)","GPU(%)","decodeFPS","droppedFrameRate(%)","AveCPUFreq(MHz)","AveGPUFreq(MHz)","MemBandwidth(MB)","pkgPower(W)")
resultFolder = getDir("Results",mode)
mkdir(resultFolder)
resultFile = getDir("Results",mode,localTime + ".xlsx")
myDiagram = diagram(resultFile,initRow,10)
tempFolder = 'localProcess'
myClientTestCfg = testConfig()

def getResult():
    emonRes = ['0','0','0']
    droppedFrameRate = '-1'
    rootPath = myClientTestCfg.localProcessPath
    for parent,dirNamesList,fileNameList in os.walk(rootPath):
        for dirName in dirNamesList:
            appendLog('----------------------------------------------------------------')
            appendLog('Current Case : %s' % dirName)
            resolution,targetFPS,frameNum,tenBitOpt,clipLength = parseClipInfo(dirName)
            tempPath = os.path.join(rootPath,dirName)
            cpuReport = os.path.join(tempPath,dirName + "_CPU_Usage.csv")
            gpuReport = os.path.join(tempPath,dirName + "_GPU_Usage.csv")
            fpsReport = os.path.join(tempPath,dirName + ".txt")
            emonReport = os.path.join(tempPath,dirName + "_Emon.csv")
            socWatchReport = os.path.join(tempPath,dirName+".csv")
            socRes = getSocRes(socWatchReport,"CPU","GPU","BW")            
            cpuUsage = getCPUUsage(cpuReport)
            gpuUsage,gpuTime = getGPUUsage(gpuReport)            
            fps = getFpsInfo(fpsReport,gpuTime,frameNum)
            if( 'chrome' in mode.lower() ):
                fpsInfo = getChromeFPS(dirName)
                appendLog("Decode FPS : %s\nDropped Frame Rate: %s" % tuple(fpsInfo) )
                fps = fpsInfo[0]
                droppedFrameRate = fpsInfo[1]
            try:
                myEmonProcessor = EmonProcessor(emonReport)
                emonRes = myEmonProcessor.run()
            except:
                print("emon raw data file no found!")
            if( socRes != ['0','0','0']):
                data = [dirName,string.atof(cpuUsage),string.atof(gpuUsage),string.atof(fps),string.atof(droppedFrameRate)] + socRes
            else:
                data = [dirName,string.atof(cpuUsage),string.atof(gpuUsage),string.atof(fps),string.atof(droppedFrameRate)] + emonRes
            myDiagram.addData(data)
        appendLog('----------------------------------------------------------------')
    myDiagram.addDiagram("CPU_Usage","B","bar")
    myDiagram.addDiagram("GPU_Usage","C","bar")
    myDiagram.addDiagram("FPS","D","line")
    myDiagram.addDiagram("Ave CPU Freq","E","line")
    myDiagram.addDiagram("Ave GPU Freq","F","line")
    myDiagram.addDiagram("Ave Mem BW","G","bar")
    myDiagram.addDiagram("Ave Pkg Power","H","bar")
    myDiagram.genDiagram()

def getTestModeInfo(testModeList):
    receiverList = None
    app = ''
    if( os.path.exists(testModeList)):
        listToRunReadHandle = open(testModeList,'r')
        case = listToRunReadHandle.readline()
        while( case[0] != '1' ):
            case = listToRunReadHandle.readline()
        listToRunReadHandle.close()
        optList = case.split(" ")
        for opt in optList:
            if( "email" in opt ):
                pos = optList.index(opt)
                receiverList = optList[pos + 1]
            if( "App" in opt):
                pos = optList.index(opt)
                appPath = optList[pos + 1]
                app = appPath.split("\\")[-1].split('\t')[0]
    return receiverList,app

if __name__ == "__main__":
    receiverList,app = getTestModeInfo("testModeList")
    getResult()
    driverVersion = getDisplayDriverVer()
    sysInfo = getSysVersion()
    osInfo = '_'.join([sysInfo['OS'],sysInfo['arch'],sysInfo['buildNum']])
    appendLog("driver Version : %s" % driverVersion)
    appendLog("os Info : %s" % osInfo)
    tempList = [driverVersion,mode,sysInfo['OS'],sysInfo['arch']]
    subject = '_'.join(tempList)
    if( receiverList ):
        handle = open('emailTemplate\\testEnv.html','r')
        content = handle.read()
        handle.close()
        content = content % (getCPUInfo(),getMemInfo(),osInfo,driverVersion,mode,app)
        sendEmail(subject,content,resultFile,receiverList)
    appendLog("The final result have been generated : %s " % resultFile )