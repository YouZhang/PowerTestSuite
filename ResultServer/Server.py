# coding = utf-8

import sys
sys.path.append('Lib')
from PowerProcessor import *
from Config import testConfig



def initEnv():
    global myConfig
    myConfig = testConfig()
    mkResFolderCMD = "mkdir " + myConfig.resultFolder
    mkRawDataPath = "mkdir " + myConfig.rawDataStoreFolder
    os.system(mkResFolderCMD)
    os.system(mkRawDataPath)

def postProcess():
    common.appendLog("backup the raw lvm data...")
    mvLVMFileCMD = 'copy RawData\*.lvm %s' % myConfig.rawDataStoreFolder
    delLVMFileCMD = 'del RawData\*.lvm'
    os.system(mvLVMFileCMD)
    os.system(delLVMFileCMD)


if __name__ == "__main__":
    initEnv()
    myPowerMem = powerDataMem()
    myProcessor = powerProcessor(myPowerMem,myConfig)
    myProcessor.process()
    postProcess()

