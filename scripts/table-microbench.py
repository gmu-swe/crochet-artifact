#!/usr/bin/python2
import re
import os
from subprocess import call

RESULTS = "../results"
SCRIPT = "../scripts/r/generateMicroTable.r"
TMP_FILE = os.path.join(RESULTS,"aggregated-micro.csv")
OUT_FILE = os.path.join(RESULTS,"table_micro.csv")

if os.path.isfile(OUT_FILE):
    os.remove(OUT_FILE)
if os.path.isfile(TMP_FILE):
    os.remove(TMP_FILE)
with open(TMP_FILE, 'w') as output:
    output.write("mode,benchmark,time,sdev\n")
    for bm in os.listdir(os.path.join(RESULTS,"microbenchmark")):
        for conf in os.listdir(os.path.join(RESULTS,"microbenchmark",bm)):
                for run in os.listdir(os.path.join(RESULTS,"microbenchmark",bm,conf)):
                    if run.startswith("out-"):
                        with open(os.path.join(RESULTS,"microbenchmark",bm,conf,run)) as file:
                            for line in file:
                                m = re.search("benchmark=([^\d]+)(\d+)} (\d+.\d+) ns;.+=(\d+.\d+)",line)
                                if m:
                                    output.write("%s,%s %s,%s,%s\n" % (conf,m.group(1),m.group(2),m.group(3),m.group(4)))
output.close()
call(["Rscript",SCRIPT,TMP_FILE,OUT_FILE])

os.remove(TMP_FILE)
