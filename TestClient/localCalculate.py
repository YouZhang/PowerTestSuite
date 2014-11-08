import sys
sys.path.append("Lib_2.0")
from testClient import testClient,getFpsInfo,getGPUUsage,getCPUUsage,getSocRes
from Config import testConfig
import os
import string
from Diagram import diagram
from common import *

initRow = ("Cases","CPU","GPU","FPS","AveCPUFreq","AveGPUFreq")
resultFile = localTime + ".xlsx"
myDiagram = diagram(resultFile,initRow,10)
tempFolder = 'localProcess'
myClientTestCfg = testConfig()

def getResult():
    rootPath = myClientTestCfg.localProcessFolder
    for parent,dirNamesList,fileNameList in os.walk(rootPath):
        for dirName in dirNamesList:
            tempPath = os.path.join(rootPath,dirName)
            cpuReport = os.path.join(tempPath,dirName + "_CPU_Usage.csv")
            gpuReport = os.path.join(tempPath,dirName + "_GPU_Usage.csv")
            fpsReport = os.path.join(tempPath,dirName + ".txt")
            socWatchReport = os.path.join(tempPath,dirName+".csv")
            socRes = getSocRes(socWatchReport,"CPU","GPU")
            fps = getFpsInfo(fpsReport)
            gpuUsage = getGPUUsage(gpuReport)
            cpuUsage = getCPUUsage(cpuReport)
            data = [dirName,string.atof(cpuUsage),string.atof(gpuUsage),string.atof(fps)] + socRes
            myDiagram.addData(data)
    myDiagram.addDiagram("CPU_Usage","B","bar")
    myDiagram.addDiagram("GPU_Usage","C","bar")
    myDiagram.addDiagram("FPS","D","line")
    myDiagram.addDiagram("Ave CPU Freq","E","line")
    myDiagram.addDiagram("Ave GPU Freq","F","line")
    myDiagram.genDiagram()

if __name__ == "__main__":
    getResult()