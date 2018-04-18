#!/usr/bin/python2

import re
import os
from subprocess import call

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

from paths import *

RESULTS  = results_root
SCRIPT   = os.path.join(os.path.dirname(__file__), "generateDacapoTable.r")
TMP_FILE = os.path.join(tables_dir,"aggregated-dacapo.csv")
OUT_FILE = os.path.join(tables_dir,"table_dacapo.csv")

if os.path.isfile(OUT_FILE):
    os.remove(OUT_FILE)
if os.path.isfile(TMP_FILE):
    os.remove(TMP_FILE)
with open(TMP_FILE, 'w') as output:
    output.write("mode,benchmark,time\n")
    for bm in os.listdir(os.path.join(RESULTS,"dacapo")):
        for conf in os.listdir(os.path.join(RESULTS,"dacapo",bm)):
            for run in os.listdir(os.path.join(RESULTS,"dacapo",bm,conf)):
                if run.startswith("out-"):
                    with open(os.path.join(RESULTS,"dacapo",bm,conf,run)) as file:
                        for line in file:
                            m = re.search("===== DaCapo 9.12 (.*) PASSED in (.*) msec =====",line)
                            if m:
                                output.write("%s,%s,%s\n" % (conf,bm,m.group(2)))
output.close()
call(["Rscript",SCRIPT,TMP_FILE,OUT_FILE])
os.remove(TMP_FILE)
