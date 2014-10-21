# coding = utf-8

import time
from PowerProcessor import *

# ('cases',"VCCIN1", "VCCIN2", "MemTotal", "DIMM")



def initEnv():
    global startButtonPos
    global stopButtonPos
    global localTime
    global resultFolder
    global resultFile
    global rawDataFilePath
    global rawDataStoreFolder
    startButtonPos = (65,55)
    stopButtonPos = (110,55)
    localTime = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())
    resultFolder = os.path.join("Results",localTime)
    resultFile = os.path.join(resultFolder,"PowerData.xlsx")
    rawDataStoreFolder = os.path.join("RawData",localTime)
    rawDataFilePath = os.path.join("RawData","test.lvm")
    mkResFolderCMD = "mkdir " + resultFolder
    mkRawDataPath = "mkdir" + rawDataStoreFolder
    os.system(mkResFolderCMD)
    os.system(mkRawDataPath)

def postProcess():
    mvLVMFileCMD = 'copy RawData\*.lvm %s' % rawDataStoreFolder
    delLVMFileCMD = 'del RawData\*.lvm'
    os.system(mvLVMFileCMD)
    os.system(delLVMFileCMD)


if __name__ == "__main__":
    #powerDataMem,inputRawData,outputFile,startButtonPos,stopButtonPos
    initEnv()
    # myPowerMem = powerDataMem()
    # myProcessor = powerProcessor(myPowerMem,rawDataFilePath,resultFile,startButtonPos,stopButtonPos)
    # myProcessor.process()
    postProcess()

