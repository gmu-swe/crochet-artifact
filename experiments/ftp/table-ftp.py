#!/usr/bin/python2
import re
import os
from subprocess import call

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

from paths import *

RESULTS  = results_root
SCRIPT   = os.path.join(os.path.dirname(__file__), "generateFTPTable.r")
TMP_FILE = os.path.join(tables_dir,"aggregated-ftp.csv")
OUT_FILE = os.path.join(tables_dir,"table_ftp.csv")

if os.path.isfile(OUT_FILE):
    os.remove(OUT_FILE)
if os.path.isfile(TMP_FILE):
    os.remove(TMP_FILE)
with open(TMP_FILE, 'w') as output:
    output.write("config,user,system,elapsed\n")
    for bm in os.listdir(os.path.join(RESULTS,"ftp")):
        for conf in os.listdir(os.path.join(RESULTS,"ftp",bm)):
            for run in os.listdir(os.path.join(RESULTS,"ftp",bm,conf)):
                if run.startswith("out-"):
                    with open(os.path.join(RESULTS,"ftp",bm,conf,run)) as file:
                        for line in file:
                            m = re.search("(\d*\.?\d*)user (\d*\.?\d*)system (\d*):(\d*\.?\d*)elapsed",line)
                            if m:
                                # print line
                                elapsed = int(m.group(3))*60+float(m.group(4))
                                output.write("%s,%s,%s,%s\n" % (conf,m.group(1),m.group(2),elapsed))
output.close()
call(["Rscript",SCRIPT,TMP_FILE,OUT_FILE])

os.remove(TMP_FILE)
