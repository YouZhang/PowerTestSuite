#coding = utf-8
import common
import os
from common import configFile
from Config import myClientTestCfg

class App(object):

    def __init__(self,appConfig):
        self.appConfig = appConfig
        self.optionsItem = configFile.getSysConfigItem("Apps",appConfig.appName,"Options")
        self.param = ''

    def getParamByType(self,type,item):
        if( item != [] ):
            try:
                item = list(item)
                for option in item:
                    if( option.tag in self.appConfig.param[type]):
                        if( option.attrib != {} ):
                            self.param += option.attrib["cmd"] + " "
                        if( '\n' not in option.text ):
                            self.param += option.text + " "
                        self.getParamByType(type,option)
            except:
                common.appendLog("parse to the tree end...")

    def genCMDParam(self):
        self.getParamByType("decoder",self.optionsItem.find("Decoder"))
        self.getParamByType("control",self.optionsItem.find("Control"))
        self.getParamByType("file",self.optionsItem.find("File"))
        self.getParamByType("display",self.optionsItem.find("Display"))

    def getFPSParam(self,targetFPS,mode):
        fpsOpt = self.optionsItem.find("Control").find("fps")
        for opt in list(fpsOpt):
            if( mode == "free" and "free" in opt.tag):
                return opt.text
            if( targetFPS in opt.tag ):
                return opt.text

    def genBatFile(self,clipName,mode):
        cmd = self.appConfig.appBinary + self.param + " > ..\log.txt"
        resolution,targetFPS,frameNum = common.parseClipInfo(clipName)
        clip = os.path.join(myClientTestCfg.clipsPath,clipName+".webm")
        fpsOpt = self.getFPSParam(targetFPS,mode)
        cmd = cmd.replace("clipName",clip).replace("targetFPS",fpsOpt).replace("log",clipName)
        batFile = os.path.join(myClientTestCfg.batFilePath,clipName+".bat")
        handle = file(batFile,'w')
        handle.write(cmd)
        handle.close()
        return resolution,targetFPS,frameNum,batFile


if __name__ == "__main__":
    pass