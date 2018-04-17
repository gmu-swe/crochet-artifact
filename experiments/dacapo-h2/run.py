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

run_native="{jdk}/bin/java {vmargs} {{benchvmargs}} -cp {dacapojar} Harness {args}"
run_crochet="{crochet}/target/jre-inst/bin/java {{benchvmargs}} {vmargs} -agentpath:{crochet}/target/libtagging.so -javaagent:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -cp {dacapojar} Harness {args}"
dacapo_opts='-C -n 50 --scratch-directory=/tmp/dacapo-scratch'
#dacapo_opts='-n 10 --scratch-directory=/tmp/dacapo-scratch'
dacapo_h2_jar='{}/benchmarks/dacapo.jar'.format(dacapoh2dir)

def workloads() :
    return {
        'default' : {
            'bin'   : '',
            'args'  : '-s default',
            'clean' : [ ],
            'env'   : { }
            } ,
        'large' : {
            'bin'   : '',
            'args'  : '-s large',
            'clean' : [ ],
            'env'   : { }
            } ,
        }

vmargs="{}".format(globalJvmParams)

# Max time any execution can take, in seconds
timeout = 5*60

pin='numactl --membind 1 --cpunodebind 1' # eg 'taskset -c 5,6,7'

def runs() :
    return {
        'native-sql' : {
            'cmd'  : run_native.format(jdk=jdk8dir,
                vmargs=vmargs,
                args='{} h2'.format(dacapo_opts),
                dacapojar=dacapo_h2_jar),
            'clean' : [ 'sudo rm -rf scratch' ],
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'crochet-sql' : {
            'cmd'  : run_crochet.format(
                crochet=crochetdir,
                vmargs=vmargs,
                args='{} h2'.format(dacapo_opts),
                dacapojar=dacapo_h2_jar),
            'clean' : [ 'sudo rm -rf scratch' ],
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'crochet' : {
            'cmd'  : run_crochet.format(
                crochet=crochetdir,
                vmargs=vmargs,
                args='{} h2-crij'.format(dacapo_opts),
                dacapojar=dacapo_h2_jar),
            'clean' : [ 'sudo rm -rf scratch' ],
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
       }

# Run everything
run(times, warmup, runs(), workloads(), timeout, os.path.join(results_root,'dacapo-h2'))
