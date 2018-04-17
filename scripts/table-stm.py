#!/usr/bin/python2
import re
import os
from subprocess import call

RESULTS = "../results"
SCRIPT = "../scripts/r/generateSTMTable.r"
TMP_FILE = os.path.join(RESULTS,"aggregated-stm.csv")
OUT_FILE = os.path.join(RESULTS,"table_stm.csv")

if os.path.isfile(OUT_FILE):
    os.remove(OUT_FILE)
if os.path.isfile(TMP_FILE):
    os.remove(TMP_FILE)
with open(TMP_FILE, 'w') as output:
    output.write("config,n\n")
    for bm in os.listdir(os.path.join(RESULTS,"stmbench7")):
        for conf in os.listdir(os.path.join(RESULTS,"stmbench7",bm)):
            for run in os.listdir(os.path.join(RESULTS,"stmbench7",bm,conf)):
                if run.startswith("out-"):
                    with open(os.path.join(RESULTS,"stmbench7",bm,conf,run)) as file:
                        for line in file:
                            m = re.search("Total throughput: (\d+.\d+) op/s ",line)
                            if m:
                                # print line
                                output.write("%s,%s\n" % (conf,m.group(1)))
output.close()
call(["Rscript",SCRIPT,TMP_FILE,OUT_FILE])

os.remove(TMP_FILE)
