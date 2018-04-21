#!/usr/bin/python2
import re
import os
from subprocess import call

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

from paths import *

RESULTS = results_root
SCRIPT = os.path.join(os.path.dirname(__file__), "generateMicroTable.r")
TMP_FILE = os.path.join(tables_dir, "aggregated-micro.csv")
OUT_FILE = os.path.join(tables_dir, "table_micro.csv")

if os.path.isfile(OUT_FILE):
    os.remove(OUT_FILE)
if os.path.isfile(TMP_FILE):
    os.remove(TMP_FILE)
with open(TMP_FILE, 'w') as output:
    output.write("mode,benchmark,time,sdev\n")
    for bm in os.listdir(os.path.join(RESULTS, "microbenchmark")):
        for conf in os.listdir(os.path.join(RESULTS, "microbenchmark", bm)):
            for run in os.listdir(os.path.join(RESULTS, "microbenchmark", bm, conf)):
                if run.startswith("out-"):
                    with open(os.path.join(RESULTS, "microbenchmark", bm, conf, run)) as file:
                        for line in file:
                            m = re.search("benchmark=([^\d]+)(\d+)} (\d+.\d+) ns;.+=(\d+.\d+)", line)
                            if m and  m.group(1).find("ConcurrentSkipListMap") == -1:
                                output.write(
                                    "%s,%s %s,%s,%s\n" % (conf, m.group(1), m.group(2), m.group(3), m.group(4)))
output.close()
call(["Rscript", SCRIPT, TMP_FILE, OUT_FILE])

os.remove(TMP_FILE)
