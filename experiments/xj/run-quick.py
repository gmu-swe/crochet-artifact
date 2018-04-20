#!/usr/bin/python2

import sys
import os

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

from run import run
from paths import *

# How many times should each run be repeated?
times = globalTimesQuick

# Number of warmup commands before starting to take measurements
warmup = 0

vmargs="{}".format(globalJvmParams)

run_xj_native="{jdk7}/bin/java \
-Dchecksum=weak \
{vmargs} \
-Dtpl.library.path={install}/xjrt/ \
-cp \
{install}/ruggedj/Benchmarks/synchroBench/resources:\
{install}/xjrt/resources:\
{install}/xj_collections/dist/xj_collections.jar:\
{install}/ruggedj/Benchmarks/synchroBench/dist/synchroBench.jar:\
{install}/transform/dist/transform.jar:\
{install}/xjrt/dist/xjrt.jar:\
{install}/ASM-5.0.3/output/dist/lib/all/asm-debug-all-4.0.jar:\
{install}/transform/lib/jode-1.1.2-pre1.jar:\
{install}/ruggedj/dist/ruggedj-generated.jar \
contention.benchmark.Test \
-b {{structure}} \
        ".format(jdk7=jdk7dir,install=install_dir,vmargs=vmargs)

run_xj_crochet="{crochetdir}/target/jre-inst/bin/java \
-Dchecksum=strict \
-DcheckRoll=crochet \
{vmargs} \
-agentpath:{crochetdir}/target/libtagging.so \
-javaagent:{crochetdir}/target/CRIJ-0.0.1-SNAPSHOT.jar \
-Xbootclasspath/p:{crochetdir}/target/CRIJ-0.0.1-SNAPSHOT.jar \
-Dtpl.library.path={install}/xjrt/ \
-cp \
{install}/ruggedj/Benchmarks/synchroBench/resources:\
{install}/xjrt/resources:\
{install}/xj_collections/dist/xj_collections.jar:\
{install}/ruggedj/Benchmarks/synchroBench/dist/synchroBench.jar:\
{install}/transform/dist/transform.jar:\
{install}/xjrt/dist/xjrt.jar:\
{install}/ASM-5.0.3/output/dist/lib/all/asm-debug-all-4.0.jar:\
{install}/transform/lib/jode-1.1.2-pre1.jar:\
{install}/ruggedj/dist/ruggedj-generated.jar \
contention.benchmark.Test \
-b {{structure}}\
        ".format(crochetdir=crochetdir,install=install_dir,vmargs=vmargs)

run_xj_xj="{install}/openjdk/build/linux-amd64/bin/java \
-Dchecksum=strict \
-DcheckRoll=xj \
{vmargs} \
-Xcomp \
-Xbatch \
-agentpath:{install}/ruggedj/jvmti_agent/jvmti_agent.lib=:=?\
-Xclassification={install}/ruggedj/Classifications/Classifications/classification_synchroBench_Linux.txt?\
-Xpartitioning={install}/ruggedj/Classifications/Partitioning/partitioning_synchroBench_Linux.txt?\
-XXJ.Optimize=true?\
-XXJ.enableHTM=false?\
-XXJ.optimizeInterfaceMethods=true?\
javaPath={install}/openjdk/build/linux-amd64/bin/java?\
tpl=-Dtpl.library.path=/home/tguest/src/xjrt/?\
classPath={install}/ruggedj/dist/ruggedj.jar:{install}/ruggedj/dist/ruggedj-bootstrap.jar:{install}/transform/dist/transform.jar:{install}/ASM-5.0.3/output/dist/lib/all/asm-debug-all-4.0.jar:{install}/xjopt/dist/xjopt.jar:{install}/xjrt/dist/xjrt.jar:{install}/transform/lib/jode-1.1.2-pre1.jar?\
outputFile=foo.txt?\
javaLibraryPath={install}/xjrt \
-Djava.system.class.loader=org.ruggedj.classloader.RuggedJSystemClassloader \
-XX:ContendedPaddingWidth=128 \
-XX:+AlwaysTenure \
-XX:+UseParallelOldGC \
-XX:+UseCondCardMark \
-DRuggedJ.GenXJ=true \
-DRuggedJ.GenRuggedJ=false \
-server \
-Dtpl.library.path={install}/xjrt/ \
-Xbootclasspath/p:\
{install}/ruggedj/dist/ruggedj.jar:\
{install}/ASM-5.0.3/output/dist/lib/all/asm-debug-all-4.0.jar:\
{install}/xjrt/dist/xjrt.jar:\
{install}/transform/dist/transform.jar:\
{install}/ruggedj/dist/ruggedj-bootstrap.jar \
-cp \
{install}/ruggedj/Benchmarks/synchroBench/resources:\
{install}/ruggedj/xjrt/resources:\
{install}/xj_collections/dist/xj_collections.jar:\
{install}/ruggedj/Benchmarks/synchroBench/dist/synchroBench.jar:\
{install}/ruggedj/transform/dist/transform.jar:\
{install}/ruggedj/xjrt/dist/xjrt.jar:\
{install}/ruggedj/ASM-5.0.3/output/dist/lib/all/asm-debug-all-4.0.jar:\
{install}/ruggedj/transform/lib/jode-1.1.2-pre1.jar:\
{install}/ruggedj/dist/ruggedj-generated.jar \
org.ruggedj.classloader.RuggedJBootstrapper \
vanguard-0 \
{install}/ruggedj/dist/Vanguard.conf \
System.out \
{install}/ruggedj/Classifications/Classifications/classification_synchroBench_Linux.txt \
{install}/ruggedj/Classifications/Partitioning/partitioning_synchroBench_Linux.txt \
contention.benchmark.Test \
-b {{structure}} \
        ".format(install=install_dir,vmargs=vmargs)


# Git commands to try
def workloads() :
    return {
        'default' : {
            'bin'   : '',
            'args'  : " -t 01"     # Number of threads
                    + " -n 2"      # Number of executions to repeat
                    + " -d 100"    # Length (ms) of each execution
                    + " -W 1"      # Warmup (sec)
                    + " -s 0"      # Snapshot operations (%, leave at 0)
                    + " -a 0"      # Write-all operations (%, leave at 0)
                    + " -i 65536"  # Size of the datastructure
                    + " -r 131072" # Range of the keys
                    + " -u 05"     # Update rate (%)
                    + " -g 0"      # Group size, how many operations per transaction
                    + " -ps CSH",  # Thread pinning, not really sure I understand this one well
            'clean' : [ ],
            'env'   : { }
            } ,
        }

# Max time any execution can take, in seconds
timeout = 10*60

pin='' # eg 'taskset -c 5,6,7'

def runs() :
    return {
        'native-seqhashset' : {
            'cmd'  : run_xj_native.format(structure="hashtables.sequential.SequentialHashIntSet"),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'native-closedhashset' : {
            'cmd'  : run_xj_native.format(structure="hashtables.xj.ClosedHashIntSet"),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'crochet-seqhashset' : {
            'cmd'  : run_xj_crochet.format(structure="hashtables.sequential.SequentialHashIntSet"),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'crochet-closedhashset' : {
            'cmd'  : run_xj_crochet.format(structure="hashtables.xj.ClosedHashIntSet"),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'xj-closedhashset' : {
            'cmd'  : run_xj_xj.format(structure="hashtables.xj.ClosedHashIntSet"),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
       }

# Run everything
run(times, warmup, runs(), workloads(), timeout, os.path.join(results_root,'xj'))
