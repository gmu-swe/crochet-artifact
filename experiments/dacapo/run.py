#!/usr/bin/python2

import sys
import os

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

from run import run
from paths import *

# How many times should each run be repeated?
times = 2

# Number of warmup commands before starting to take measurements
warmup = 0

run_native="{jdk}/bin/java {vmargs} {{benchvmargs}} -cp {dacapojar} Harness {args}"
run_crochet="{crochet}/target/jre-inst/bin/java {{benchvmargs}} {vmargs} -agentpath:{crochet}/target/libtagging.so -javaagent:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -cp {dacapojar} Harness {args}"
run_crochet_cb="{crochet}/target/jre-inst/bin/java {{benchvmargs}} {vmargs} -agentpath:{crochet}/target/libtagging.so -javaagent:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -cp {dacapojar}:{crochet}/exp-scripts/lib/CRIJ-dacapoCB-0.0.1-SNAPSHOT.jar Harness {args}"

def workloads() :
    return {
        'avrora' : {
            'bin'   : '',
            'args'  : "avrora",
            'clean' : [ ],
            'env'   : { }
            } ,
        'batik' : {
            'bin'   : '',
            'args'  : "batik",
            'clean' : [ ],
            'env'   : { }
            } ,
        'eclipse' : {
            'bin'   : '',
            'args'  : "eclipse",
            'vmargs': { 'native': "\
 -Declipse.java.home={jdk7}\
 -javaagent:{crochet}/exp-scripts/lib/dacapo-eclipse-hacker-0.0.1-SNAPSHOT.jar\
 -Xbootclasspath/p:{crochet}/exp-scripts/lib/dacapo-eclipse-hacker-0.0.1-SNAPSHOT.jar\
 ".format(jdk7=jdk7dir, crochet=crochetdir),
                        'crochet': "-Declipse.java.home={jdk7}/jre".format(jdk7=jdk7dir),
                        },
            'clean' : [ ],
            'env'   : { }
            } ,
        'fop' : {
            'bin'   : '',
            'args'  : "fop",
            'clean' : [ ],
            'env'   : { }
            } ,
        'h2' : {
            'bin'   : '',
            'args'  : "h2",
            'clean' : [ ],
            'env'   : { }
            } ,
        'jython' : {
            'bin'   : '',
            'args'  : "jython",
            'clean' : [ ],
            'env'   : { }
            } ,
        'luindex' : {
            'bin'   : '',
            'args'  : "luindex",
            'clean' : [ ],
            'env'   : { }
            } ,
        'lusearch' : {
            'bin'   : '',
            'args'  : "lusearch",
            'clean' : [ ],
            'env'   : { }
            } ,
        'pmd' : {
            'bin'   : '',
            'args'  : "pmd",
            'clean' : [ ],
            'env'   : { }
            } ,
        'sunflow' : {
            'bin'   : '',
            'args'  : "sunflow",
            'clean' : [ ],
            'env'   : { }
            } ,
        'tomcat' : {
            'bin'   : '',
            'args'  : "tomcat",
            'clean' : [ ],
            'env'   : { }
            } ,
        'tradebeans' : {
            'bin'   : '',
            'args'  : "tradebeans",
            'clean' : [ ],
            'env'   : { }
            } ,
        'tradesoap' : {
            'bin'   : '',
            'args'  : "tradesoap",
            'clean' : [ 'rm -rf /experiments/luis-crochet/crochet-artifact/scratch' ],
            'env'   : { }
            } ,
        'xalan' : {
            'bin'   : '',
            'args'  : "xalan",
            'clean' : [ ],
            'env'   : { }
            } ,
        }

vmargs="-Xmx10G"

# Max time any execution can take, in seconds
timeout = 10*60

pin='numactl --membind 1 --cpunodebind 1' # eg 'taskset -c 5,6,7'

def runs() :
    return {
        'native' : {
            'cmd'  : run_native.format(jdk=jdk8dir,
                vmargs=vmargs,
                args='--variance 2.0 -C -n 50',
                dacapojar=dacapojar),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'crochet' : {
            'cmd'  : run_crochet.format(
                jdk8=jdk8dir,
                crochet=crochetdir,
                vmargs=vmargs,
                args='--variance 2.0 -C -n 50',
                dacapojar=dacapojar),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'crochet-callback' : {
            'cmd'  : run_crochet_cb.format(
                crochet=crochetdir,
                vmargs=vmargs,
                args='--variance 2.0 -C -n 50 -c net.jonbell.crij.CheckpointingCB',
                dacapojar=dacapojar),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
       }

# Run everything
run(times, warmup, runs(), workloads(), timeout, os.path.join(results_root,'dacapo'))
