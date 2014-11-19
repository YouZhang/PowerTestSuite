#coding = utf-8
import string
from common import appendLog

class EmonProcessor(object):

    def __init__(self,emonRawData):
        self.rawDataHandle = open(emonRawData,'r')
        self.getDataIndex()
        self.curTime = 0
        self.curPkgPower = 0
        self.deltaTime = 0
        self.preTime = 0
        self.prePkgPower = 0
        self.powerSum = 0
        self.index = 0
        self.avePower = 0
        self.IAFreqSum = 0
        self.GTFreqSum = 0
        self.getOneLineData()

    def getOneLineData(self):
        dataList = self.rawDataHandle.readline().split(',')
        powerUnitTemp = dataList[self.powerUnitIndex]
        IAFreqTemp = dataList[self.iaFreqIndex]
        GTFreqTemp = dataList[self.gtFreqIndex]
        self.preTime = self.curTime
        self.prePkgPower = self.curPkgPower
        self.curTime = string.atof(dataList[self.timeIndex])
        self.powerUnit = int(powerUnitTemp[len(powerUnitTemp)-4:len(powerUnitTemp)-2],16)
        self.IAFreq = int(IAFreqTemp[len(IAFreqTemp)-4:len(IAFreqTemp)-2],16) * 100
        if(len(GTFreqTemp) == 6):
            self.GTFreq = int(GTFreqTemp[0:4],16) * 50
        else:
            self.GTFreq = int(GTFreqTemp[0:3],16) * 50
        self.curPkgPower = int(dataList[self.pkgPowerIndex],16)

    def getDataIndex(self):
        dataTitleList = self.rawDataHandle.readline().split(',')
        for i in range(len(dataTitleList)):
            if "Time" in dataTitleList[i]:
                self.timeIndex = i
            elif("PowerUnit" in dataTitleList[i]):
                self.powerUnitIndex = i
            elif("PKG_Power" in dataTitleList[i]):
                self.pkgPowerIndex = i
            elif("GTFreq" in dataTitleList[i]):
                self.gtFreqIndex = i
            elif("IAFreq" in dataTitleList[i]):
                self.iaFreqIndex = i

    def getInstantData(self):
        deltaPower = self.curPkgPower - self.prePkgPower
        deltaTime = self.curTime -self.preTime
        instantPower = float(deltaPower) / pow(2,self.powerUnit) * (1000000/deltaTime)
        self.IAFreqSum += self.IAFreq
        self.GTFreqSum += self.GTFreq
        self.powerSum += instantPower
        self.index += 1.0

    def run(self):
        avePower = 'XXX'
        aveIAFreq = 'XXX'
        memBW = 'XXX'
        aveGTFreq = 'XXX'
        while(True):
            try:
                self.getOneLineData()
                self.getInstantData()
            except:
                self.rawDataHandle.close()
                appendLog("parse emon raw data to the end...")
                avePower = self.powerSum / self.index
                aveIAFreq = self.IAFreqSum / self.index
                aveGTFreq = self.GTFreqSum / self.index
                appendLog("average pkg power : %s" % avePower)
                appendLog("average IA Freq : %s" % aveIAFreq)
                appendLog("average GT Freq : %s" % aveGTFreq)
                break
        return [aveIAFreq,aveGTFreq,memBW,avePower]


if __name__ == "__main__":
    myEmonProcessor = EmonProcessor("Avengers_1080p_25fps_100frame_100kbps_m8.csv")
    myEmonProcessor.run()