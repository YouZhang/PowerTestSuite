#coding = utf-8
from common import getDir,localTime,appendLog,getIp
from SystemInfo import getSysVersion
from xml.etree import ElementTree as ET

class appConfig(object):

    def __init__(self,mode):
        appPath = testModeCfgFile.getConfigContent(mode,"AppPath")
        appBin = testModeCfgFile.getConfigContent(mode,"AppBin")
        serverName = testModeCfgFile.getConfigContent(mode,"ServerMachine")
        ip = getIp(serverName)
        port = int(testModeCfgFile.getConfigContent(mode,"Port"))
        self.address = (ip,port)
        self.appName = testModeCfgFile.getConfigContent(mode,"AppName")
        self.regFile = testModeCfgFile.getConfigContent(mode,"RegFile")
        self.driver = testModeCfgFile.getConfigContent(mode,"Driver")
        self.runList = " "           
        self.appBinary = getDir(appPath,appBin) + " "
        self.param = {}
        self.param["decoder"] = testModeCfgFile.getConfigContent(mode,"Decoder")
        self.param["file"] = testModeCfgFile.getConfigContent(mode,"File")
        self.param["display"] = testModeCfgFile.getConfigContent(mode,"Display")
        self.param["control"] = testModeCfgFile.getConfigContent(mode,"Control")
        self.optionsItem = appOptFile.getSysConfigItem(self.appName,"Options")

class testConfig(object):

    def __init__(self):
        self.getFilePathCfg()
        self.getMiscCfg()

    def getFilePathCfg(self):
        self.driverPath = sysConfigFile.getConfigContent("Path","DriverPath")
        self.appPath = sysConfigFile.getConfigContent("Path","AppPath")
        self.clipsPath = sysConfigFile.getConfigContent("Path","ClipsPath")
        self.batFilePath = sysConfigFile.getConfigContent("Path","batFilePath")
        self.localProcessPath = sysConfigFile.getConfigContent("Path","localProcessPath")
        self.socResPath = sysConfigFile.getConfigContent("Path","SocResPath")
        self.backupPath = sysConfigFile.getConfigContent("Path","BackupPath")
        self.regFilePath = sysConfigFile.getConfigContent("Path","RegPath")
        self.logFilePath = sysConfigFile.getConfigContent("Path","LogPath")
        self.logFile = getDir(self.logFilePath,localTime+".txt")

    def getMiscCfg(self):
        self.powerConfig = sysConfigFile.getConfigContent("DefaultConfig","PowerConfig")
        self.hangService = sysConfigFile.getConfigContent("DefaultConfig","AppHangService")
        self.tempFolder = sysConfigFile.getConfigContent("DefaultConfig","TempFolder")
        self.MVP = sysConfigFile.getConfigContent("DefaultConfig","MVP")
        self.restartSvr = sysConfigFile.getConfigContent("DefaultConfig","RestartSvr")
        self.socWatch = sysConfigFile.getConfigContent("DefaultConfig","SocWatch")
        self.emon = sysConfigFile.getConfigContent("DefaultConfig","Emon")
        self.powerMeasure = sysConfigFile.getConfigContent("DefaultConfig","powerMeasure")
        self.sleepTime = int(sysConfigFile.getConfigContent("DefaultConfig","SleepTime"))
        self.osArch = getSysVersion()['arch'][0:2]
        self.driver = None

class configFile(object):

    def __init__(self,xmlFile):
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

def initConfigFile():
    global sysConfigFile
    global appOptFile
    global testModeCfgFile
    sysConfigFile = configFile("configXML\\SysConfig.xml")
    appOptFile = configFile("configXML\\testAppOpt.xml")
    testModeCfgFile = configFile("configXML\\testModeConfig.xml")

initConfigFile()

if __name__ == "__main__":
    configFile.getSysConfigItem("Apps","mv_decoder_adv")
    myConfig = appConfig("fixedPlayback")
    pass
