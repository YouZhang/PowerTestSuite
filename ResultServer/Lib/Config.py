#coding = utf-8
from xml.etree import ElementTree as ET
import os
import common

class sysConfigFile(object):

    def __init__(self,xmlFile = 'sysConfig.xml'):
        self.rootNode = ET.parse(xmlFile).getroot()

    def getSysConfigItem(self,type,tag):
        item = self.rootNode.find(type).findall(tag)[0].text
        return item


class testConfig(object):

    def __init__(self):
        configFile = sysConfigFile()
        ip = configFile.getSysConfigItem("Misc","Address")
        port = int(configFile.getSysConfigItem("Misc","Port"))
        # ip address config
        self.address = (ip,port)
        # folder config
        self.resultFolder = configFile.getSysConfigItem("Misc","resultFolder")
        self.resultFile = os.path.join(self.resultFolder,common.localTime+".xlsx")
        self.rawDataStoreFolder = configFile.getSysConfigItem("Misc","rawDataFolder")
        self.rawDataFilePath = os.path.join(self.rawDataStoreFolder,"test.lvm")
        self.LogFilePath = configFile.getSysConfigItem("Misc","LogPath")
        # start Button & end Button config
        self.startButtonPos = tuple(configFile.getSysConfigItem("Misc","startButtonPos").split())
        self.stopButtonPos = tuple(configFile.getSysConfigItem("Misc","stopButtonPos").split())
        # diagram config
        self.initRow = tuple(configFile.getSysConfigItem("Misc","initRow").split())
        self.chartType = configFile.getSysConfigItem("Misc","chartType")
        self.chartStyle = int(configFile.getSysConfigItem("Misc","chartStyle"))
        self.targetDataPos = configFile.getSysConfigItem("Misc","targetDataPos")