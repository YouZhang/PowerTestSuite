#coding = utf-8
import socket
import os
from common import appendLog
import time

runList = os.path.join("RunList","list_ToRun.txt")
doneList = os.path.join("RunList","list_done.txt")
# address = ('10.239.141.154', 31500)
address = ('127.0.0.1', 31500)

def addStartupService():
    command = 'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v Client /t reg_sz /d "F:\SHU\PowerTestSuite\TestClient\client.py" /f'
    os.system(command)

def removeStartupService():
    command = 'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v client /f'
    os.system(command)

def restartOS():
    command = 'shutdown -r'
    os.system(command)

def writeClips(fromFile,toFile):
    toRunListHandle = open(toFile,'w')
    doneListHandle = open(fromFile,'r')
    clips = doneListHandle.read()
    toRunListHandle.write(clips)
    toRunListHandle.close()
    doneListHandle.close()

if __name__ == "__main__":

    while True:

        addStartupService()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listToRunReadHandle = open('RunList\List_ToRun.txt','r')
        clipsToRunList = listToRunReadHandle.readlines()
        listToRunReadHandle.close()

        if( clipsToRunList != [] ):
            clipNameToRun = clipsToRunList[0].strip('\n')
            appendLog("Current test clip : %s" % clipNameToRun)
            sock.sendto(clipNameToRun, address)
            batFileName =  clipNameToRun + '.bat'
            os.system(batFileName)        
            sock.sendto(clipNameToRun,address)  # end signal sent
            appendLog("%s  power test end..." % clipNameToRun)
            context = ''.join(clipsToRunList[1:len(clipsToRunList)])
            listToRunWriteHandle = open('RunList\List_ToRun.txt','w')
            listToRunWriteHandle.write(context)
            listToRunWriteHandle.close()
            sock.close()
            time.sleep(60)
            appendLog("will restart....")
            # restartOS()
        else:
            writeClips(doneList,runList)
            sock.sendto("done",address)
            appendLog( "all clips power test done!\nremoving startup service...")
            # removeStartupService()
            appendLog("Power test finished...")
            break


