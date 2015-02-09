import os
import getpass
import glob
import sys
sys.path.append('Lib_2.0')
from common import cmdRun,syncRun,waitProc
from SystemInfo import getSysVersion
pwd = os.getcwd()

def readFile(fileName):
    handle = open(fileName,'rb')
    content = handle.read()
    handle.close()
    return content

def writeFile(content,fileName):
    handle = open(fileName,'wb')
    handle.write(content)
    handle.close()

def enableAutoLogin():
    currUser = getpass.getuser()
    password = getpass.getpass('Enter password for user : %s \nPassword : ' % currUser)
    regFileTemp = 'reg\\autoLoginTemp.reg'
    targetRegFile = 'reg\\autoLogin.reg'
    content = readFile(regFileTemp)
    content = content % (currUser,password)
    writeFile(content,targetRegFile)

def enableSocWatch():
    msiFiles = glob.glob('tool\socwatch\WDTF\Win*.msi')
    for msiFile in msiFiles:
        cmd = 'msiexec /i "%s"' % msiFile
        cmdRun(cmd)

def enableEmon():
    osArch = getSysVersion()['arch'][0:2]
    infFile = 'tool\emon\%s\EMonDriverDevice.inf' % osArch
    cmd = 'enableEmon.bat %s' % infFile
    cmdRun(cmd)

def installApp(path):
    syncRun(path)    
    
def unzip( zipFile, destFile ):
    cmd = 'mkdir "%s"' % destFile
    cmdRun(cmd)
    print('Please wait when unzipping 7z...')
    cmdRun('tool\\7z.exe x %s -o"%s"' % (zipFile, destFile))
    print('Finish')
    return destFile
    
def enableVCLib():
    vcredistFiles = glob.glob('tool\\vcredist*.exe')
    for binary in vcredistFiles:
        installApp(binary)
        waitProc('vcredist')
        
if __name__ == '__main__':
    enableAutoLogin()
    enableSocWatch()
    enableEmon()
    enableVCLib()
    installApp('tool\potplayer\PotPlayerSetup.exe')    
    waitProc('PotP')
    installApp('tool\potplayer\PotPlayerSetup64.exe')
    waitProc('PotP')
    installApp('tool\PowerDVD\Setup.exe')
    waitProc('Setu')
    unzip('tool\chromium.7z','C:\chromium')