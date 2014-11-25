# coding = utf-8

import sys
sys.path.append('Lib')
from PowerProcessor import *
from Config import testConfig
from common import *
import threading

# testMode = {
# vp9MvPerfTestCfg : "VP9MvFreePlayback",
# vp9ChromeTestCfg : "VP9FixedChrome",
# vp9FixedTestCfg : "VP9FixedPlayback",
# hevcFixedTestCfg : "HEVCFixedPlayback"
# }



def initEnv(testMode):
    myConfig = testConfig(testMode)
    mkdir(myConfig.resultFolder)
    mkdir(myConfig.rawDataStoreFolder)
    mkdir(myConfig.logFilePath)
    mkdir(myConfig.rawDataBackupFolder)
    return myConfig

def postProcess(rawDataBackupFolder):
    appendLog("backup the raw lvm data...")
    copy("RawData\*.lvm",rawDataBackupFolder)
    removeFiles("RawData\*.lvm")

def powerMeasure(mode):
    while True:
        myConfig = initEnv(mode)
        myPowerMem = powerDataMem()
        myProcessor = powerProcessor(myPowerMem,myConfig)
        myProcessor.process()
        postProcess(myConfig.rawDataBackupFolder)

if __name__ == "__main__":

    threadsList = []
    # testModeList = ["VP9MvFreePlayback","VP9FixedChrome","VP9FixedPlayback","HEVCFixedPlayback"]
    testModeList = ["HEVCFixedPlayback"]
    for mode in testModeList:
        thread = threading.Thread(target=powerMeasure,args=(mode,))
        threadsList.append(thread)

    for thread in threadsList:
        thread.setDaemon(True)
        thread.start()

    thread.join()
