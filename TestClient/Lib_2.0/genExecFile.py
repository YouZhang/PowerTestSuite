#coding = utf-8
from distutils.core import setup
import py2exe
import sys

script = ['..\localCalculate.py','..\PnPTestSuite_Beta1_0.py','downloadDriver.py','..\enableApp_InternalOnly.py']

options = {"py2exe":

    {"compressed": 1,
     "optimize": 2,     
     "bundle_files": 1 }
    }

for i in range( len(script) ):
    setup(
        options = options,
        zipfile=None,
        console=[{"script": "%s" % script[i] }]
        )