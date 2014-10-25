# coding = utf-8
import xlsxwriter

class diagram(object):

    def __init__(self,resultFile,initRow,chartType,chartStyle):
        self.workBook = xlsxwriter.Workbook(resultFile)
        self.workSheet = self.workBook.add_worksheet()
        self.workSheet.write_row(0,0,initRow)
        self.chartStyle = chartStyle
        self.chartType = chartType
        self.row = 0

    def addData(self,data):
        self.row += 1
        self.workSheet.write_row(self.row,0,data)

    def genDiagram(self):
        lineChart = self.workBook.add_chart({'type': self.chartType})
        series = {
            'categories' : '=Sheet1!$A$2:$A$'+str(self.row + 1) ,
            'values' : '=Sheet1!$F$2:$F$' + str(self.row + 1)
        }
        lineChart.add_series(series)
        lineChart.set_style(self.chartStyle)
        self.workSheet.insert_chart(self.row + 2,0, lineChart, {'x_offset': 10, 'y_offset': 10})
        self.workBook.close()

def testDiagram():
    myDiagram = diagram("test.xlsx")
    myDiagram.addData([22,23,24,25])
    myDiagram.addData([22,23,24,25])
    myDiagram.addData([22,23,24,25])
    myDiagram.addData([22,23,24,25])
    myDiagram.genDiagram()