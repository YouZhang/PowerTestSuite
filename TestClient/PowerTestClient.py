import sys
import os
sys.path.append("Lib_2.0")
from testClient import testClient
from Config import myClientTestCfg


def init():
    cmd = "del Perf*"
    userChoice = raw_input("Are you sure that delete all Perf data?(Y OR N)")
    if( userChoice == 'y' or userChoice == 'Y'):
        os.system(cmd)


if __name__ == "__main__":
    init()
    myTestClient = testClient(myClientTestCfg)
    myTestClient.run()
