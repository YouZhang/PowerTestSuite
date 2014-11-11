#coding = utf-8
import common
import os
from Config import testConfig

myClientTestCfg = testConfig()

class App(object):

    def __init__(self,appConfig):
        self.appConfig = appConfig
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
        self.getParamByType("display",self.appConfig.optionsItem.find("Display"))
        self.getParamByType("decoder",self.appConfig.optionsItem.find("Decoder"))
        self.getParamByType("control",self.appConfig.optionsItem.find("Control"))
        self.getParamByType("file",self.appConfig.optionsItem.find("File"))


    def getFPSParam(self,targetFPS,mode):
        fpsOpt = self.appConfig.optionsItem.find("Control").find("fps")
        fpsParam = None
        for opt in list(fpsOpt):
            if( targetFPS in opt.tag ):
                fpsParam = opt.text
            if( "Free" in mode and "free" in opt.tag):
                fpsParam =  opt.text
        return fpsParam

    def genTenBitParam(self,targetTenBit):
        tenBitOpt = self.appConfig.optionsItem.find("File").find("Bit10")
        if( targetTenBit in tenBitOpt.tag):
            self.param += tenBitOpt.text

    def genBatFile(self,clipName,targetFPS,tenBitOpt,mode):
        self.genTenBitParam(tenBitOpt)
        cmd = self.appConfig.appBinary + self.param + " > log.txt"
        clip = os.path.join(myClientTestCfg.clipsPath,clipName)
        fpsOpt = self.getFPSParam(targetFPS,mode)
        if( fpsOpt != None):
            cmd = cmd.replace("targetFPS",fpsOpt)
        cmd = cmd.replace("clipName",clip).replace("log",clipName).replace("pwd",os.getcwd())
        batFile = os.path.join(myClientTestCfg.batFilePath,clipName+".bat")
        handle = file(batFile,'w')
        handle.write(cmd)
        handle.close()
        return batFile

if __name__ == "__main__":
    pass