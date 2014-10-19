#coding = utf-8
import socket
import os
import time

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

def appendLog(message):
    print message
    logFile = open("Log\PowerTestLog.txt","r+")
    logFile.write(message +"\n")
    logFile.close()


runList = "RunList\list_ToRun.csv"
doneList = "RunList\list_ToRun.csv"
address = ('127.0.0.1', 31500)

if __name__ == "__main__":

    while True:

        addStartupService()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listToRunReadHandle = open('RunList\List_ToRun.txt','r')
        clipsToRunList = listToRunReadHandle.readlines()
        listToRunReadHandle.close()
        clipNameToRun = clipsToRunList[0].strip('\n')
        if( clipNameToRun ):
            appendLog("Current test clip : %s" % clipNameToRun)
            sock.sendto(clipNameToRun, address)
            batFileName = clipNameToRun + '.bat'
            os.system(batFileName)
            appendLog("%s  test end..." % clipNameToRun)
            sock.sendto(clipNameToRun,address)  # end signal sent
            time.sleep(2)
            context = ''.join(clipsToRunList[1:len(clipsToRunList)])
            listToRunWriteHandle = open('RunList\List_ToRun.txt','w')
            listToRunWriteHandle.write(context)
            listToRunWriteHandle.close()
            sock.close()
            appendLog("will restart....")
            # restartOS()
        else:
            writeClips(doneList,runList)
            sock.sendto("done",address)
            appendLog( "all clips power test done!\nremoving startup service...")
            removeStartupService()
            sock.sendto(clipNameToRun, address)
            appendLog("Power test finished...")
        time.sleep(100)

