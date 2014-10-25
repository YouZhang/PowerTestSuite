import sys
sys.path.append("Lib")
from PowerProcessor import *
from Config import testConfig
from Config import sysConfigFile
import glob


def initEnv():
    global myConfig
    myConfig = testConfig()


def getLvmFileList():
    configFile = sysConfigFile()
    path = configFile.getSysConfigItem("Misc","localDataPath")
    filesType = path + "\\*.lvm"
    lvmFileList = glob.glob(filesType)
    return lvmFileList

if __name__ == "__main__":
    initEnv()
    lvmFileList = getLvmFileList()
    mem = powerDataMem()
    localProcessor = powerProcessor(mem,myConfig)
    localProcessor.localProcess(lvmFileList)