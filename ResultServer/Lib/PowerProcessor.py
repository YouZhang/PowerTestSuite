import socket
import string
import os
import common
from Diagram import diagram

class powerDataMem(object):

    def __init__(self):
        self.VCCIN1_dv = 0
        self.VCCIN1_V = 0
        self.VCCIN2_dv = 0
        self.VCCIN2_V = 0
        self.MemTotal_dv = 0
        self.MemTotal_V = 0
        self.DIMM_dv = 0
        self.DIMM_V = 0
        self.index = 0


    def addRawData(self, rawDataList):
        self.VCCIN1_dv += rawDataList[0]
        self.VCCIN1_V += rawDataList[1]
        self.VCCIN2_dv += rawDataList[3]
        self.VCCIN2_V += rawDataList[4]
        self.MemTotal_dv += rawDataList[6]
        self.MemTotal_V += rawDataList[7]
        self.DIMM_dv += rawDataList[9]
        self.DIMM_V += rawDataList[10]
        self.index += 1


    def getFinalResult(self):
        VCCIN1_dvAve = self.VCCIN1_dv / self.index
        VCCIN1_VAve = self.VCCIN1_V / self.index
        VCCIN2_dvAve = self.VCCIN2_dv / self.index
        VCCIN2_VAve = self.VCCIN2_V / self.index
        Mem_dvAve = self.MemTotal_dv / self.index
        Mem_VAve = self.MemTotal_V / self.index
        DIMM_dvAve = self.DIMM_dv / self.index
        DIMM_VAve = self.DIMM_V / self.index
        VCCIN1Power = VCCIN1_dvAve * VCCIN1_VAve / 0.001995
        VCCIN2Power = VCCIN2_dvAve * VCCIN2_VAve / 0.002
        MemPower = Mem_dvAve * Mem_VAve / 0.002
        DIMMPower = DIMM_dvAve * DIMM_VAve / 0.002
        TotalPower = VCCIN1Power + VCCIN2Power + MemPower - DIMMPower
        return [VCCIN1Power, VCCIN2Power, MemPower, DIMMPower,TotalPower]


class powerProcessor(object):

    def __init__(self, powerDataMem,myConfig):
        self.powerMem = powerDataMem
        self.inputRawData = myConfig.rawDataFilePath
        self.chartType = myConfig.chartType
        self.resultDiagram = diagram(myConfig.resultFile,myConfig.initRow,myConfig.chartType)
        self.address = myConfig.address
        self.startButtonPos = myConfig.startButtonPos
        self.stopButtonPos = myConfig.stopButtonPos
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)
        self.targetDataPos = myConfig.targetDataPos
        self.isCapturing = False

    def getDataFromLVM(self,lvmFile):
        parseFlag = False
        try:
            with open(lvmFile, 'r') as rawDataFile:
                for line in rawDataFile:
                    if ( parseFlag ):
                        rawDataList = line.split()
                        rawDataList = map(lambda data: string.atof(data), rawDataList)
                        self.powerMem.addRawData(rawDataList)
                    if ("X_Value" in line):
                        parseFlag = True
            return self.powerMem.getFinalResult()
        except:
            common.appendLog( "error in opening lvm file")
            exit(-1)

    def startCapture(self):
        common.mouseClick(int(self.startButtonPos[0]),int(self.startButtonPos[1]))

    def stopCapture(self):
        common.mouseClick(int(self.stopButtonPos[0]),int(self.stopButtonPos[1]))

    def process(self):
        while True:
            common.appendLog("receiving start/stop tag from client...")
            case, addr = self.sock.recvfrom(2048)
            if not case:
                common.appendLog("client has exist")
                break
            common.appendLog("received: %s tag from %s" % (case, addr) )
            lvmFile = self.inputRawData
            if("end" in case):
                common.appendLog("all cases finished...\nResult diagram will be generated")
                break
            elif(not self.isCapturing):
                self.isCapturing = True
                common.appendLog("start capturing %s power data..." % case)
                self.startCapture()
            else:
                self.isCapturing = False
                self.stopCapture()
                common.appendLog("stop capturing %s power data..." % case)
                lvmFile = renameFile(lvmFile,case)
                powerData = self.getDataFromLVM(lvmFile)
                message = "VCCIN1 : %s\nVCCIN2 : %s\nMemToal : %s\nDIMM : %s\nTotalPower:%s" % tuple(powerData)
                common.appendLog(message)
                powerData.insert(0,case)
                self.resultDiagram.addData(powerData)
                self.powerMem.__init__()
                common.appendLog("--------------------------------------------------------------")
        self.sock.close()
        self.resultDiagram.addDiagram("PowerData",self.targetDataPos,self.chartType)
        self.resultDiagram.genDiagram()

    def localProcess(self,lvmFileList):
        self.powerMem.__init__()
        for lvmFile in lvmFileList:
            common.appendLog("processing %s ..." % lvmFile)
            powerData = self.getDataFromLVM(lvmFile)
            message = "VCCIN1 : %s\nVCCIN2 : %s\nMemTotal : %s\nDIMM : %s\nTotalPower:%s" % tuple(powerData)
            common.appendLog(message)
            powerData.insert(0,lvmFile)
            self.resultDiagram.addData(powerData)
            common.appendLog("--------------------------------------------------------------")
            self.powerMem.__init__()
        self.resultDiagram.addDiagram("PowerData",self.targetDataPos,self.chartType)
        self.resultDiagram.genDiagram()

def renameFile(beforeName,newName):
    targetFile = 'RawData\%s.lvm' % newName
    renameCMD = "move %s %s" % (beforeName,targetFile)
    print renameCMD
    os.system(renameCMD)
    return targetFile