import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import wmi
import os

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

def sendEmail(subject,content,resultFile,receiverList):
    resultFileName = resultFile.split("\\")[-1]
    msg = MIMEMultipart()
    att1 = MIMEText(open('%s' % resultFile, 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="*"'.replace("*",resultFileName)
    msg.attach(att1)
    txt = MIMEText(content,'html')     
    msg.attach(txt)
    strTo = receiverList.split(',')
    msg['to'] = ','.join(strTo)
    print msg['to']
    msg['from'] = 'CodecPnP.TestSuite@intel.com'
    msg['subject'] = subject

    try:
        server = smtplib.SMTP()
        server.connect('smtp.intel.com')
        server.sendmail(msg['from'], strTo ,msg.as_string())
        server.quit()
        print 'Email send successfully!!'
    except Exception, e:
        print str(e)