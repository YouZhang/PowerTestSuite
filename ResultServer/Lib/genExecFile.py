#coding = utf-8
from distutils.core import setup
import py2exe
import sys

scripts = ['..\server.py','..\localCalculate.py']

options = {"py2exe":

    {"compressed": 1,
     "optimize": 2,     
     "bundle_files": 1 }
    }
for script in scripts:
    setup(
        options = options,
        zipfile=None,
        console=[{"script": "%s" % script }]
        )