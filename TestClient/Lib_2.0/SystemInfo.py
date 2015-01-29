import wmi
import os
import glob
import re

def readFile(fileName):
    handle = open(fileName,'r')
    content = handle.read()
    handle.close()
    return content

def writeFile(content,fileName):
    handle = open(fileName,'w')
    handle.write(content)
    handle.close()

def getSysVersion():
    sysInfo = {}
    c = wmi.WMI ()
    for system in c.Win32_OperatingSystem():
        sysInfo["OS"] = system.Caption.encode("UTF8")
        sysInfo["buildNum"] = system.BuildNumber
        sysInfo["arch"] = system.OSArchitecture.encode("UTF8")
    return sysInfo

def getCPUInfo():
    c = wmi.WMI ()
    for processor in c.Win32_Processor():
        print "Process Name: %s" % processor.Name.strip()
    return processor.Name.strip()

def getMemInfo():
    totalMem = 0
    c = wmi.WMI ()
    for Memory in c.Win32_PhysicalMemory():
        print "Memory Capacity: %.fMB" %(int(Memory.Capacity)/1048576)
        totalMem += int(Memory.Capacity)/1048576
    return totalMem

def getDriverVersion(driver):
    command = 'tool\PnPutil.exe -e'
    driverInfo = os.popen(command).readlines()
    for line in driverInfo:
        if(driver in line):
            pos = driverInfo.index(line)
            driverVersion = driverInfo[pos + 1].replace('\n','')
            return driverVersion
    return None

def matchPatten(content,patten,pos=0):
    patten = re.compile(patten)
    matchedItem = patten.findall(content,pos)
    if( matchedItem ):
        return matchedItem[0]
    else:
        return None

def getDisplayDriverVer():
    infFile = glob.glob('C:\Windows\System32\DriverStore\FileRepository\igdlh*\igdlh*.inf')[0]
    content = readFile(infFile)
    patten = '.*"(\w+-\w+-\d+)".*'
    driverLabel = matchPatten(content,patten)
    return driverLabel

if __name__ == '__main__':
    getDisplayDriverVer()
