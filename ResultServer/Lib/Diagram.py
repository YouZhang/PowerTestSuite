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

    def addDiagram(self,targetDataPos):
        chart = self.workBook.add_chart({'type': self.chartType})
        series = {
            'categories' : '=Sheet1!$A$2:$A$'+str(self.row + 1) ,
            'values' : '=Sheet1!$targetDataPos$2:$targetDataPos$'.replace("targetDataPos",targetDataPos) + str(self.row + 1)
        }
        chart.set_legend({'position': 'top'})
        chart.add_series(series)
        chart.set_style(self.chartStyle)
        self.workSheet.insert_chart(self.row + 2,0, chart, {'x_offset': 10, 'y_offset': 10})

    def genDiagram(self):
        self.workBook.close()
