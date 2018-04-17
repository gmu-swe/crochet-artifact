#!/usr/bin/python2
import re
import os
from subprocess import call

RESULTS = "../results"
SCRIPT = "../scripts/r/generateDacapoTable.r"
TMP_FILE = os.path.join(RESULTS,"aggregated-dacapo.csv")
OUT_FILE = os.path.join(RESULTS,"table_dacapo.csv")

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
