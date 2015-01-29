#coding = utf-8
from common import getDir,appendLog,pwd


class App(object):

    def __init__(self,appConfig,testCfg):
        self.appConfig = appConfig
        self.testCfg = testCfg
        self.param = ''

    def getParamByType(self,type,item):
        if( item != [] ):
            try:
                item = list(item)
                for option in item:
                    if( option.tag in self.appConfig.param[type].split()):
                        if( option.attrib != {} ):
                            self.param += option.attrib["cmd"] + " "
                        if( '\n' not in option.text ):
                            self.param += option.text + " "
                        self.getParamByType(type,option)
            except:
                appendLog("parse to the tree end...")

    def genCMDParam(self):
        self.getParamByType("display",self.appConfig.optionsItem.find("Display"))
        self.getParamByType("decoder",self.appConfig.optionsItem.find("Decoder"))
        self.getParamByType("file",self.appConfig.optionsItem.find("File"))
        self.getParamByType("control",self.appConfig.optionsItem.find("Control"))
        
    def getFPSParam(self,targetFPS,mode):
        fpsOpt = self.appConfig.optionsItem.find("Control").find("fps")
        fpsParam = None
        for opt in list(fpsOpt):
            if( str(targetFPS) in opt.tag ):
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

        cmd = self.appConfig.appBinary + self.param + ' > "log.txt" 2>&1'
        clip = getDir(self.testCfg.clipsPath,clipName)
      
        fpsOpt = self.getFPSParam(targetFPS,mode)
        if( fpsOpt != None):
            cmd = cmd.replace("targetFPS",fpsOpt)
        cmd = cmd.replace("clipName",clip).replace("log",clipName).replace("pwd",pwd)
        # if( "PDVD" in mode ):
        #     cmd = getDir(pwd,clip)+'.mkv > %s.txt' % clip
        batFile = getDir(self.testCfg.batFilePath,clipName.replace(' ','_')+".bat")
        handle = file(batFile,'w')
        handle.write(cmd)
        handle.close()

if __name__ == "__main__":
    pass