#!/usr/bin/python2
import re
import os
from subprocess import call

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

from paths import *

RESULTS = results_root
SCRIPT   = os.path.join(os.path.dirname(__file__), "generateSTMTable.r")
TMP_FILE = os.path.join(tables_dir,"aggregated-stm.csv")
OUT_FILE = os.path.join(tables_dir,"table_stm.csv")

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
