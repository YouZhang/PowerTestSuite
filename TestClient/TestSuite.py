import sys
sys.path.append("Lib_2.0")
from testClient import testClient,removeStartupService
from Config import testConfig
from common import *
# mode = {
# vp9MvPerfTestCfg : "VP9MvFreePlayback",
# vp9ChromeTestCfg : "VP9FixedChrome",
# vp9FixedTestCfg : "VP9FixedPlayback",
# hevcFixedTestCfg : "HEVCFixedPlayback"
#FFPlay
# }

def init():
    testCfg = testConfig()
    removeFiles("Perf*")
    removeFiles("*.yuv")
    createFolders(testCfg)
    return testCfg

def createFolders(testCfg):
    '''
    :param testCfg:  object
    :return:
    '''
    mkdir(testCfg.batFilePath)
    mkdir(testCfg.logFilePath)
    mkdir(testCfg.backupPath)
    mkdir(testCfg.localProcessPath)
    mkdir(testCfg.driverPath)
    mkdir(testCfg.socResPath)

if __name__ == "__main__":
    testModeList = "testModeList"
    while True:
        modeToRunList,mode,paramList =  getRunCase(testModeList)
        if( mode != None):
            myClientTestCfg = init()
            myTestClient = testClient(myClientTestCfg, mode)
            myTestClient.overrideTestConfig(paramList)
            myTestClient.run()
            removeDoneCase(testModeList,modeToRunList,mode)
            appendLog("----------------------------------------------")
        else:
            appendLog("all test mode finished...")
            removeStartupService()
            break
