# coding = utf-8

import sys
sys.path.append('Lib')
from PowerProcessor import *


class testConfig(object):

    def __init__(self):
        self.startButtonPos = (65,55)
        self.stopButtonPos = (110,55)
        self.resultFolder = os.path.join("Results",common.localTime)
        self.resultFile = os.path.join(self.resultFolder,"PowerData.xlsx")
        self.rawDataStoreFolder = os.path.join("RawData",common.localTime)
        self.rawDataFilePath = os.path.join("RawData","test.lvm")
        # self.address = ('127.0.0.1', 31500)
        self.address = ('10.239.141.154', 31500)

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

