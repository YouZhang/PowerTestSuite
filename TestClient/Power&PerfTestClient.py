import sys
import os
sys.path.append("Lib_2.0")
from testClient import testClient
from Config import testConfig



def init():
    cmd = "del Perf*"
    os.system(cmd)


if __name__ == "__main__":
    init()
    myClientTestCfg = testConfig()
    myTestClient = testClient(myClientTestCfg,"VP9FreePlayback")
    myTestClient.run()
