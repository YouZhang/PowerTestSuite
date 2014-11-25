import sys
sys.path.append("Lib")
from PowerProcessor import *
from Config import testConfig
from Config import sysConfigFile
import glob


def initEnv(testMode):
    global myConfig
    myConfig = testConfig(testMode)


def getLvmFileList():
    configFile = sysConfigFile()
    path = configFile.getConfigContent("CommonCfg","localDataPath")
    filesType = path + "\\*.lvm"
    lvmFileList = glob.glob(filesType)
    return lvmFileList

if __name__ == "__main__":
    testMode = sys.argv[1]
    initEnv(testMode)
    lvmFileList = getLvmFileList()
    mem = powerDataMem()
    localProcessor = powerProcessor(mem,myConfig)
    localProcessor.localProcess(lvmFileList)