# coding = utf-8
import socket
import string
import xlsxwriter


# ('cases',"VCCIN1", "VCCIN2", "MemTotal", "DIMM")

def appendLog(message):

    print message
    logFile = open("Log\PowerTestLog.txt","r+")
    logFile.write(message + "\n")
    logFile.close()

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
        return [VCCIN1Power, VCCIN2Power, MemPower, DIMMPower]


class powerProcessor():

    def __init__(self, powerDataMem):

        self.powerMem = powerDataMem
        self.address = ('127.0.0.1', 31500)
        self.isCapturing = False
        self.resultDiagram = diagram()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)

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
            appendLog( "error in lvm file")
            exit(-1)

    def process(self):

        while True:
            appendLog("reciving tag from client...")
            case, addr = self.sock.recvfrom(2048)
            if not case:
                appendLog("client has exist")
                break
            appendLog("received: %s from %s" % (case, addr) )
            lvmFile = case + ".lvm"
            if("end" in case):
                appendLog("all cases finished...\nResult diagram will be generated")
                break
            elif(not self.isCapturing):
                self.isCapturing = True
                appendLog("start capturing power data...")
                startCapture()
                moveFile(lvmFile)
            else:
                self.isCapturing = False
                stopCapture()
                powerData = self.getDataFromLVM(lvmFile)
                self.resultDiagram.addData(case,powerData)

        self.sock.close()
        self.resultDiagram.genDiagram()


class diagram(object):

    def __init__(self):
        self.workBook = xlsxwriter.Workbook('PowerData__.xlsx')
        self.workSheet = self.workBook.add_chartsheet()
        self.workSheet.write_row(0,0,('cases','VCCIN1','VCCIN2','MemTotal','DIMM'))
        self.row = 0

    def addData(self,case,powerData):
        self.row += 1
        powerData.insert(0,case)
        self.workSheet.write_row(0,self.row,powerData)

    def genDiagram(self):
        lineChart = self.workBook.add_chart({'type': 'line'})
        series = {
            'categories' : '=Sheet1!$A$1:$A$3',
            'values' : '=Sheet1!$B$1:$B$3'
        }
        lineChart.add_series(series)
        lineChart.set_style(10)
        self.workSheet.insert_chart('F2', lineChart, {'x_offset': 25, 'y_offset': 10})
        self.workBook.close()

def startCapture():
    pass


def stopCapture():
    pass

def moveFile(clip):
    pass

rawDataPath = "Raw_Data\\test.lvm"

if __name__ == "__main__":

    myPowerMem = powerDataMem()
    myProcessor = powerProcessor(myPowerMem)
    myProcessor.process()
