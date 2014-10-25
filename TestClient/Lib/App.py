import common
from xml.etree import ElementTree as ET
import os

class App(object):

    def __init__(self,name):
        self.Name = name
        self.app = getSysConfig("Apps",self.Name)
        self.getBinary()

    def getBinary(self):
        self.Binary = self.app.attrib['path'] + self.app.find("Binary").text

    def getCmdParam(self,params):
        if( params != None):
            targetNode = None
            for i in range(len(params)):
                if(i == 0):
                    targetNode = self.app.find(params[0])
                else:
                    targetNode = targetNode.find(params[i])
            return targetNode.text

    def generateCMD(self,param):
        cmd = self.Binary + param
        return cmd

    def generateBatFile(self,cmd,clipName):
        clipPath = getSysConfig("Path","ClipsPath").text
        clip = os.path.join(clipPath,clipName)
        cmd = cmd.replace("%s",clip)
        batName = clipName + '.bat'
        handle = file(batName,'w')
        handle.write(cmd)
        handle.close()



class appConfig(object):

    def __init__(self):
        self.AsyncFreePlay = ("AsyncMode","Freerun")
        self.AsyncFixed30 = ("AsyncMode","FixedFPS","Thirty")
        self.AsyncFixed60 = ("AsyncMode","FixedFPS","Sixty")
        self.DecodeFree = ("Decode","Freerun")
        self.DecodeFixed30 = ("Decode","Fixed","Thirty")
        self.DecodeFixed60 = ("Decode","Fixed","Sixty")
        self.SyncFreePlay = ("SyncMode","Freerun")
        self.SyncFixed30 = ("SyncMode","FixedFPS","Thirty")
        self.SyncFixed60 = ("SyncMode","FixedFPS","Sixty")



def getSysConfig(type,tag,xmlFile = 'SysConfig.xml'):
    try:
        tree = ET.parse(xmlFile)
        root = tree.getroot()
    except Exception,e:
        common.appendLog("Error : can not parse the xml file")
        return -1
    item = root.find(type).findall(tag)[0]
    return item

def appProcess(appName,clipName):
    myConfig = appConfig()
    testApp = App(appName)
    cmdParam = testApp.getCmdParam(myConfig.AsyncFreePlay)
    cmd = testApp.generateCMD(cmdParam)
    testApp.generateBatFile(cmd,clipName)


if __name__ == "__main__":
    appProcess("mv_decoder_adv","ToS_1080p_30fps_VP9_2200f_tilec4r4_3000kbps")