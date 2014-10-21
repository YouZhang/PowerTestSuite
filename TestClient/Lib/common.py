#coding = utf-8


import time
import os


localTime = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())

def appendLog(message):
    print message
    logfile = os.path.join("Log",localTime+".log")
    logHandle = open(logfile,"a")
    logHandle.write(message + "\n\n")
    logHandle.close()


if __name__ == "__main__":
    pass