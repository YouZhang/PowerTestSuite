import sys
sys.path.append("Lib")
from testClient import testClient
from Config import myClientTestCfg


if __name__ == "__main__":
    myTestClient = testClient(myClientTestCfg)
    myTestClient.run()
