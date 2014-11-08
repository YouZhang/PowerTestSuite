#coding = utf-8

import os
import common
from common import sysConfigFile

configFile = sysConfigFile()

class appConfig(object):

    def __init__(self,mode):
        appPath = configFile.getConfigContent("AppConfig",mode,"AppPath")
        appBin = configFile.getConfigContent("AppConfig",mode,"AppBin")
        self.appName = configFile.getConfigContent("AppConfig",mode,"AppName")
        self.regFile = configFile.getConfigContent("AppConfig",mode,"RegFile")
        self.optionsItem = configFile.getSysConfigItem("Apps",self.appName,"Options")
        self.appBinary = os.path.join(appPath,appBin) + " "
        self.param = {}
        self.param["decoder"] = configFile.getConfigContent("AppConfig",mode,"Decoder")
        self.param["file"] = configFile.getConfigContent("AppConfig",mode,"File")
        self.param["display"] = configFile.getConfigContent("AppConfig",mode,"Display")
        self.param["control"] = configFile.getConfigContent("AppConfig",mode,"Control")

class testConfig(object):

    def __init__(self):        
        logPath = configFile.getConfigContent("Path","LogPath")
        runListPath = configFile.getConfigContent("Path","RunListPath")
        ip = configFile.getConfigContent("Misc","IP")
        port = int(configFile.getConfigContent("Misc","Port"))
        self.address = (ip,port)
        self.appPath = configFile.getConfigContent("Path","AppPath")
        self.clipsPath = configFile.getConfigContent("Path","ClipsPath")
        self.logFile = os.path.join(logPath,common.localTime+".txt")
        self.todoList = os.path.join(runListPath,"List_ToRun.txt")
        self.doneList = os.path.join(runListPath,"List_Done.txt")
        self.batFilePath = configFile.getConfigContent("Path","batFilePath")
        self.localProcessFolder = configFile.getConfigContent("Path","localProcessPath")
        self.powerConfig = configFile.getConfigContent("Misc","PowerConfig")
        self.hangService = configFile.getConfigContent("Misc","AppHangService")
        self.MVP = configFile.getConfigContent("Misc","MVP")
        self.restartSvr = configFile.getConfigContent("Misc","RestartSvr")
        self.socWatch = configFile.getConfigContent("Misc","SocWatch")



if __name__ == "__main__":
    configFile.getSysConfigItem("Apps","mv_decoder_adv")
    myConfig = appConfig("fixedPlayback")
    pass
