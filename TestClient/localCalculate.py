import sys
sys.path.append("Lib_")
from testClient import testClient,getFpsInfo,getGPUUsage,getCPUUsage,myDiagram
from Config import myClientTestCfg
import os
import string


def getResult():
    rootPath = myClientTestCfg.localProcessFolder
    for parent,dirNamesList,fileNameList in os.walk(rootPath):
        for dirName in dirNamesList:
            tempPath = os.path.join(rootPath,dirName)
            cpuReport = os.path.join(tempPath,dirName + "_CPU_Usage.csv")
            gpuReport = os.path.join(tempPath,dirName + "_GPU_Report.csv")
            fpsReport = os.path.join(tempPath,dirName + ".txt")
            fps = 'xxx'
            fps = getFpsInfo(fpsReport)
            gpuUsage = getGPUUsage(gpuReport)
            cpuUsage = getCPUUsage(cpuReport)
            data = [dirName,string.atof(cpuUsage),string.atof(gpuUsage),fps]
            myDiagram.addData(data)
    myDiagram.addDiagram("B")
    myDiagram.addDiagram("C")
    myDiagram.genDiagram()

if __name__ == "__main__":
    getResult()