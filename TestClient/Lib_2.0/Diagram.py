# coding = utf-8
import xlsxwriter

class diagram(object):

    def __init__(self,resultFile,initRow,chartStyle):
        self.workBook = xlsxwriter.Workbook(resultFile)
        self.workSheet = self.workBook.add_worksheet()
        self.workSheet.write_row(0,0,initRow)
        self.chartStyle = chartStyle
        self.row = 0
        self.chartInsertPos = 0

    def addData(self,data):
        self.row += 1
        self.chartInsertPos += 1
        self.workSheet.write_row(self.row,0,data)

    def addDiagram(self,chartName,targetDataPos,chartType):
        chart = self.workBook.add_chart({'type': chartType})
        chart.set_title({'name': chartName})
        series = {
            'categories' : '=Sheet1!$A$2:$A$'+str(self.row + 1) ,
            'values' : '=Sheet1!$targetDataPos$2:$targetDataPos$'.replace("targetDataPos",targetDataPos) + str(self.row + 1),
            'data_labels': {'value': True}
        }
        chart.set_legend({'none': True})
        # chart.set_legend({'position': 'top'})
        chart.add_series(series)
        chart.set_style(self.chartStyle)
        self.workSheet.insert_chart(self.chartInsertPos + 2,0, chart, {'x_offset': 10, 'y_offset': 10})
        self.chartInsertPos += 15

    def genDiagram(self):
        self.workBook.close()