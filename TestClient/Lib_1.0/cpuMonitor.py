#coding = utf-8
import psutil
import os
import time

class CPUMonitor(object):

    def __init__(self):
        pass
        
    def taskMonitor(self):
        cpuUtilization = psutil.cpu_percent(4)
        if( cpuUtilization < 5 ):
            print "current CPU Utilization: %s" % cpuUtilization
            killFirefox = "taskkill -f -im firefox.exe"
            killChrome = "taskkill -f -im chrome.exe"
            print("kill firefox...")
            os.system(killFirefox)
            print("kill chrome...")
            os.system(killChrome)
            
            
if __name__ == "__main__":
    cpuMonitor = CPUMonitor()
    time.sleep(10)
    while(1):
        cpuMonitor.taskMonitor()
        time.sleep(5)