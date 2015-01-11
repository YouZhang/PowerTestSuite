import sys
sys.path.append("Lib_2.0")
from testClient import testClient,getFpsInfo,getGPUUsage,getCPUUsage,getSocRes
from Config import testConfig
import os
import string
from Diagram import diagram
from common import *
from emon import EmonProcessor

try:
    mode = sys.argv[1]
except:
    mode = "ChromeFixedPlayback"
    
initRow = ("Cases","CPU","GPU","FPS","AveCPUFreq","AveGPUFreq","MemBandwidth","pkgPower")
resultFolder = getDir("Results",mode)
mkdir(resultFolder)
resultFile = getDir("Results",mode,localTime + ".xlsx")
myDiagram = diagram(resultFile,initRow,10)
tempFolder = 'localProcess'
myClientTestCfg = testConfig()

def getResult():
    emonRes = ['0','0','0']
    rootPath = myClientTestCfg.localProcessPath
    for parent,dirNamesList,fileNameList in os.walk(rootPath):
        for dirName in dirNamesList:
            clipResolution,targetFPS,frameNum,tenBitOpt = parseClipInfo(dirName)
            tempPath = os.path.join(rootPath,dirName)
            cpuReport = os.path.join(tempPath,dirName + "_CPU_Usage.csv")
            gpuReport = os.path.join(tempPath,dirName + "_GPU_Usage.csv")
            fpsReport = os.path.join(tempPath,dirName + ".txt")
            emonReport = os.path.join(tempPath,dirName + "_Emon.csv")
            socWatchReport = os.path.join(tempPath,dirName+".csv")
            socRes = getSocRes(socWatchReport,"CPU","GPU","BW")            
            gpuUsage,gpuTime = getGPUUsage(gpuReport)
            fps = getFpsInfo(fpsReport,gpuTime,frameNum)
            cpuUsage = getCPUUsage(cpuReport)
            try:
                myEmonProcessor = EmonProcessor(emonReport)
                emonRes = myEmonProcessor.run()
            except:
                print("emon raw data file no found!")
            if( socRes != ['0','0','0']):
                data = [dirName,string.atof(cpuUsage),string.atof(gpuUsage),string.atof(fps)] + socRes
            else:
                data = [dirName,string.atof(cpuUsage),string.atof(gpuUsage),string.atof(fps)] + emonRes
            myDiagram.addData(data)
    myDiagram.addDiagram("CPU_Usage","B","bar")
    myDiagram.addDiagram("GPU_Usage","C","bar")
    myDiagram.addDiagram("FPS","D","line")
    myDiagram.addDiagram("Ave CPU Freq","E","line")
    myDiagram.addDiagram("Ave GPU Freq","F","line")
    myDiagram.addDiagram("Ave Mem BW","G","bar")
    myDiagram.addDiagram("Ave Pkg Power","H","bar")
    myDiagram.genDiagram()

if __name__ == "__main__":
    getResult()