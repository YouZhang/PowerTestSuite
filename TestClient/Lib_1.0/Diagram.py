# coding = utf-8
import xlsxwriter

class diagram(object):

    def __init__(self,resultFile,initRow):
        self.workBook = xlsxwriter.Workbook(resultFile)
        self.workSheet = self.workBook.add_worksheet()
        self.workSheet.write_row(0,0,initRow)
        self.row = 0

    def addData(self,case,data):
        self.row += 1
        data.insert(0,case)
        self.workSheet.write_row(self.row,0,data)

    def genDiagram(self):
        # lineChart = self.workBook.add_chart({'type': 'line'})
        # series = {
        #     'categories' : '=Sheet1!$A$2:$A$'+str(self.row + 1) ,
        #     'values' : '=Sheet1!$col$2:$$'.replace("%s",) + str(self.row + 1)
        # }
        # lineChart.add_series(series)
        # lineChart.set_style(10)
        # self.workSheet.insert_chart(self.row + 2,0, lineChart, {'x_offset': 10, 'y_offset': 10})
        self.workBook.close()

def testDiagram():
    myDiagram = diagram("test.xlsx")
    myDiagram.addData("1",[22,23,24,25])
    myDiagram.addData("2",[22,23,24,25])
    myDiagram.addData("3",[22,23,24,25])
    myDiagram.addData("4",[22,23,24,25])
    myDiagram.genDiagram()