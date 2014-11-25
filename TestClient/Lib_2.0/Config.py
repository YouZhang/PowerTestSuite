#coding = utf-8
from common import getDir,localTime,appendLog,getIp
from xml.etree import ElementTree as ET

class appConfig(object):

    def __init__(self,mode):
        appPath = configFile.getConfigContent("TestMode",mode,"AppPath")
        appBin = configFile.getConfigContent("TestMode",mode,"AppBin")
        serverName = configFile.getConfigContent("TestMode",mode,"ServerMachine")
        ip = getIp(serverName)
        port = int(configFile.getConfigContent("TestMode",mode,"Port"))
        self.address = (ip,port)
        self.appName = configFile.getConfigContent("TestMode",mode,"AppName")
        self.regFile = configFile.getConfigContent("TestMode",mode,"RegFile")
        self.optionsItem = configFile.getSysConfigItem("Apps",self.appName,"Options")
        self.driver = configFile.getConfigContent("TestMode",mode,"Driver")
        self.runList = configFile.getConfigContent("TestMode",mode,"RunList")
        self.appBinary = getDir(appPath,appBin) + " "
        self.param = {}
        self.param["decoder"] = configFile.getConfigContent("TestMode",mode,"Decoder")
        self.param["file"] = configFile.getConfigContent("TestMode",mode,"File")
        self.param["display"] = configFile.getConfigContent("TestMode",mode,"Display")
        self.param["control"] = configFile.getConfigContent("TestMode",mode,"Control")

class testConfig(object):

    def __init__(self):
        self.getFilePathCfg()
        self.getMiscCfg()

    def getFilePathCfg(self):
        self.runListPath = configFile.getConfigContent("Path","RunListPath")
        self.driverPath = configFile.getConfigContent("Path","DriverPath")
        self.appPath = configFile.getConfigContent("Path","AppPath")
        self.clipsPath = configFile.getConfigContent("Path","ClipsPath")
        self.batFilePath = configFile.getConfigContent("Path","batFilePath")
        self.localProcessPath = configFile.getConfigContent("Path","localProcessPath")
        self.socResPath = configFile.getConfigContent("Path","SocResPath")
        self.backupPath = configFile.getConfigContent("Path","BackupPath")
        self.logFilePath = configFile.getConfigContent("Path","LogPath")
        self.logFile = getDir(self.logFilePath,localTime+".txt")

    def getMiscCfg(self):
        self.powerConfig = configFile.getConfigContent("Misc","PowerConfig")
        self.hangService = configFile.getConfigContent("Misc","AppHangService")
        self.tempFolder = configFile.getConfigContent("Misc","TempFolder")
        self.MVP = configFile.getConfigContent("Misc","MVP")
        self.restartSvr = configFile.getConfigContent("Misc","RestartSvr")
        self.socWatch = configFile.getConfigContent("Misc","SocWatch")
        self.emon = configFile.getConfigContent("Misc","Emon")
        self.powerMeasure = configFile.getConfigContent("Misc","powerMeasure")

class sysConfigFile(object):

    def __init__(self,xmlFile = 'sysConfig.xml'):
        self.rootNode = ET.parse(xmlFile).getroot()

    def getSysConfigItem(self,*args):
        item = self.rootNode.find(args[0])
        for i in range(1,len(args)):
            item = item.find(args[i])
        return item

    def getConfigContent(self,*args):
        try:
            item = self.getSysConfigItem(*args)
            res = item.text
            return res
        except AttributeError:
            appendLog(args)
            appendLog("error input parameter, cannot find your param in config file")
            exit(-1)

    def getConfigTag(self,*args):
        item = self.getSysConfigItem(*args)
        return item.tag

configFile = sysConfigFile()

if __name__ == "__main__":
    configFile.getSysConfigItem("Apps","mv_decoder_adv")
    myConfig = appConfig("fixedPlayback")
    pass
