#coding = utf-8
import psutil
import os
import time

localTime = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())

def appendLog(message):
    print message
    logfile = localTime + ".txt"
    logHandle = open(logfile,"a")
    logHandle.write(message + "\n\n")
    logHandle.close()

class CPUMonitor(object):

    def __init__(self):
        pass
        
    def taskMonitor(self):
        cpuUtilization = psutil.cpu_percent(2.3)
        print cpuUtilization
        if( cpuUtilization < 5 ):
            appendLog("current CPU Utilization: %s" % cpuUtilization)
            killFirefox = "taskkill -f -im firefox.exe"
            killChrome = "taskkill -f -im chrome.exe"
            killMv = "taskkill -f -im mv_decoder_adv*"
            killMfx = "taskkill -f -im mfx_player*"
            killSoc = "taskkill -f -im socwatch.exe"
            killEmon = "taskkill -f -im Emon*"
            appendLog("kill socWatch...")
            os.system(killSoc)
            appendLog("kill Emon...")
            os.system(killEmon)  
            appendLog("kill mv_decoder_adv..")
            os.system(killMv)
            appendLog("kill mfx_player..")
            os.system(killMfx)
            appendLog("kill firefox...")
            os.system(killFirefox)
            appendLog("kill chrome...")
            os.system(killChrome)
        
            

def killHangAppService():
    cpuMonitor = CPUMonitor()
    time.sleep(10)
    while(1):
        cpuMonitor.taskMonitor()
        time.sleep(5)

if __name__ == "__main__":
    cpuMonitor = CPUMonitor()
    time.sleep(10)
    while(1):
        cpuMonitor.taskMonitor()
        time.sleep(1.8)