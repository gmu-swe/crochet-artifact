#!/usr/bin/python2

import sys
import os

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

from run import run
from paths import *

# How many times should each run be repeated?
times = globalTimes

# Number of warmup commands before starting to take measurements
warmup = 0

vmargs="{}".format(globalJvmParams)

run_bench="{jdk}/bin/java {vmargs} {{benchvmargs}} -jar {jar}/target/CRIJ-Microbench-0.0.1-SNAPSHOT.jar --vm '{{benchvm}}' {opts} {{benchclass}}".format(
        jar=microbenchdir,
        jdk=jdk8dir,
        vmargs=vmargs,
        opts='--timeUnit ms',
        )

jdk_vm="{}/bin/java".format(jdk8dir)
crochet_vm="{crochet}/target/jre-inst/bin/java -agentpath:{crochet}/target/libtagging.so -javaagent:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar".format(crochet=crochetdir)
criu_vm="{jdk}/bin/java -agentpath:{crochet}/target/libcriu.so -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar".format(jdk=jdk8dir,crochet=crochetdir)

def workloads() :
    return {
        'default' : {
            'bin'   : '',
            'args'  : '',
            'clean' : [ ],
            'env'   : { }
            } ,
        }

# Max time any execution can take, in seconds
timeout = 15*60

pin='numactl --membind 1 --cpunodebind 1' # eg 'taskset -c 5,6,7'

def runs() :
    return {
        'no-check-no-sum-native' : {
            'cmd'  : run_bench.format(
                benchvm=jdk_vm,
                benchvmargs='',
                benchclass='net.jonbell.bench.NoCheckpointBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'no-check-sum-native' : {
            'cmd'  : run_bench.format(
                benchvm=jdk_vm,
                benchvmargs='-Dchecksum',
                benchclass='net.jonbell.bench.NoCheckpointBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'no-check-no-sum-crochet' : {
            'cmd'  : run_bench.format(
                benchvm=crochet_vm,
                benchvmargs='',
                benchclass='net.jonbell.bench.NoCheckpointBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'no-check-sum-crochet' : {
            'cmd'  : run_bench.format(
                benchvm=crochet_vm,
                benchvmargs='-Dchecksum',
                benchclass='net.jonbell.bench.NoCheckpointBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'check-no-sum-crochet' : {
            'cmd'  : run_bench.format(
                benchvm=crochet_vm,
                benchvmargs='',
                benchclass='net.jonbell.bench.CheckpointCrochetBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'check-sum-crochet' : {
            'cmd'  : run_bench.format(
                benchvm=crochet_vm,
                benchvmargs='-Dchecksum',
                benchclass='net.jonbell.bench.CheckpointCrochetBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'check-no-sum-serial' : {
            'cmd'  : run_bench.format(
                benchvm=jdk_vm,
                benchvmargs='',
                benchclass='net.jonbell.bench.CheckpointSerializationBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'check-sum-serial' : {
            'cmd'  : run_bench.format(
                benchvm=jdk_vm,
                benchvmargs='-Dchecksum',
                benchclass='net.jonbell.bench.CheckpointSerializationBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'check-sum-cloner' : {
            'cmd'  : run_bench.format(
                benchvm=jdk_vm,
                benchvmargs='-Dchecksum',
                benchclass='net.jonbell.bench.DeepCloneBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'check-sum-mapcloner' : {
            'cmd'  : run_bench.format(
                benchvm=jdk_vm,
                benchvmargs='-Dchecksum',
                benchclass='net.jonbell.bench.HashMapDeepCloneBench',
                ),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'check-sum-criu' : {
            'cmd'  : run_bench.format(
                benchvm=criu_vm,
                benchvmargs='-Dchecksum',
                benchclass='net.jonbell.bench.CheckpointCRIUBench',
                ),
            'wrap' : 'sudo -E {}'.format(pin),
            'env'  : { },
            },
       }

# Run everything
run(times, warmup, runs(), workloads(), timeout, os.path.join(results_root,'microbenchmark'))
