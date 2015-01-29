#coding = utf-8
import psutil
import os
import time

localTime = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())

def killProcess(procName):
    print 'kill %s' % procName
    os.system('taskkill /f /im %s*' % procName)
    
class CPUMonitor(object):

    def __init__(self):
        pass
        
    def taskMonitor(self):
        cpuUtilization = psutil.cpu_percent(5)
        print "current cpu utilization : %s" % cpuUtilization
        if( cpuUtilization < 4.5 ):
            print("current CPU Utilization: %s" % cpuUtilization)
            killProcess('soc')
            killProcess('emon')
            killProcess('mv_decoder_adv')
            killProcess('mfx_player')

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
        time.sleep(4.8)