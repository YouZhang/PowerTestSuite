#coding = utf-8
from xml.etree import ElementTree as ET
from common import getDir,getIp,localTime,appendLog,mkdir

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


class testConfig(object):

    def __init__(self,testMode):
        configFile = sysConfigFile()
        serverName = configFile.getConfigContent("CommonCfg","ServerMachine")
        ip = getIp(serverName,testMode)
        port = int(configFile.getConfigContent("SpecificCfg",testMode,"Port"))               
        self.address = (ip,port)
        self.rawDataFilePath = getDir(self.rawDataStoreFolder,"test.lvm")
        # folder config
        self.logFilePath = configFile.getConfigContent("SpecificCfg",testMode,"LogPath")
        self.resultFolder = configFile.getConfigContent("SpecificCfg",testMode,"resultFolder")        
        self.rawDataStoreFolder = configFile.getConfigContent("CommonCfg","rawDataFolder")        
        self.rawDataBackupFolder = getDir(self.rawDataStoreFolder,localTime)
        # start Button & end Button config
        self.startButtonPos = tuple(configFile.getConfigContent("CommonCfg","startButtonPos").split())
        self.stopButtonPos = tuple(configFile.getConfigContent("CommonCfg","stopButtonPos").split())
        # diagram config
        self.resultFile = getDir(self.resultFolder,localTime+".xlsx")
        self.initRow = tuple(configFile.getConfigContent("CommonCfg","initRow").split())
        self.chartType = configFile.getConfigContent("CommonCfg","chartType")
        self.chartStyle = int(configFile.getConfigContent("CommonCfg","chartStyle"))
        self.targetDataPos = configFile.getConfigContent("CommonCfg","targetDataPos")
        self.initFolder()
        
    def initFolder():
        mkdir(self.resultFolder)
        mkdir(self.resultFolder)
        mkdir(self.rawDataStoreFolder)
        mkdir(self.rawDataBackupFolder)
