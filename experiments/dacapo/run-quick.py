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

run_native="{jdk}/bin/java {vmargs} {{benchvmargs}} -Xbootclasspath/p:{crochet}/exp-scripts/lib/dacapo-eclipse-hacker-0.0.1-SNAPSHOT.jar -cp {dacapojar} Harness {args}"
run_crochet="{crochet}/target/jre-inst/bin/java {{benchvmargs}} {vmargs} -agentpath:{crochet}/target/libtagging.so -javaagent:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar:{crochet}/exp-scripts/lib/dacapo-eclipse-hacker-0.0.1-SNAPSHOT.jar -cp {dacapojar} Harness {args}"
run_crochet_cb="{crochet}/target/jre-inst/bin/java {{benchvmargs}} {vmargs} -agentpath:{crochet}/target/libtagging.so -javaagent:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar:{crochet}/exp-scripts/lib/dacapo-eclipse-hacker-0.0.1-SNAPSHOT.jar -cp {dacapojar}:{crochet}/exp-scripts/lib/CRIJ-dacapoCB-0.0.1-SNAPSHOT.jar Harness {args}"
run_criu_cb="{jdk}/bin/java {{benchvmargs}} {vmargs} -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar:{crochet}/exp-scripts/lib/dacapo-eclipse-hacker-0.0.1-SNAPSHOT.jar -agentpath:{crochet}/target/libcriu.so -cp {dacapojar}:{crochet}/exp-scripts/lib/CRIJ-dacapoCB-0.0.1-SNAPSHOT.jar Harness {args}"

def workloads() :
    return {
        'avrora' : {
            'bin'   : '',
            'args'  : "avrora -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'batik' : {
            'bin'   : '',
            'args'  : "batik -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'eclipse' : {
            'bin'   : '',
            'args'  : "eclipse -s small",
            'vmargs': "-Declipse.java.home={jdk7}/jre/\
                       -javaagent:{crochet}/exp-scripts/lib/dacapo-eclipse-hacker-0.0.1-SNAPSHOT.jar\
                       ".format(jdk7=jdk7dir, crochet=crochetdir),
            'clean' : [ ],
            'env'   : { }
            } ,
        'fop' : {
            'bin'   : '',
            'args'  : "fop -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'h2' : {
            'bin'   : '',
            'args'  : "h2 -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'jython' : {
            'bin'   : '',
            'args'  : "jython -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'luindex' : {
            'bin'   : '',
            'args'  : "luindex -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'lusearch' : {
            'bin'   : '',
            'args'  : "lusearch -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'pmd' : {
            'bin'   : '',
            'args'  : "pmd -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'sunflow' : {
            'bin'   : '',
            'args'  : "sunflow -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'tomcat' : {
            'bin'   : '',
            'args'  : "tomcat -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'tradebeans' : {
            'bin'   : '',
            'args'  : "tradebeans -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        'tradesoap' : {
            'bin'   : '',
            'args'  : "tradesoap -s small",
            'clean' : [ 'rm -rf /experiments/luis-crochet/crochet-artifact/scratch' ],
            'env'   : { }
            } ,
        'xalan' : {
            'bin'   : '',
            'args'  : "xalan -s small",
            'clean' : [ ],
            'env'   : { }
            } ,
        }

# Max time any execution can take, in seconds
timeout = 10*60

pin='' # eg 'taskset -c 5,6,7'

def runs() :
    return {
        'native' : {
            'cmd'  : run_native.format(jdk=jdk8dir,
                crochet=crochetdir,
                vmargs=vmargs,
                args='-n 1',
                dacapojar=dacapojar),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'crochet' : {
            'cmd'  : run_crochet.format(
                jdk8=jdk8dir,
                crochet=crochetdir,
                vmargs=vmargs,
                args='-n 1',
                dacapojar=dacapojar),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'crochet-callback' : {
            'cmd'  : run_crochet_cb.format(
                crochet=crochetdir,
                vmargs=vmargs,
                args='-n 1 -c net.jonbell.crij.CheckpointingCB',
                dacapojar=dacapojar),
            'wrap' : '{}'.format(pin),
            'env'  : { },
            },
        'criu-callback' : {
            'cmd'  : run_criu_cb.format(
                jdk=jdk8dir,
                crochet=crochetdir,
                vmargs=vmargs,
                args='-n 1 -c net.jonbell.crij.CRIUCB',
                dacapojar=dacapojar),
            'clean' : [ 'sudo rm -rf {}/*'.format(criudir) ],
            'wrap' : 'sudo -E {}'.format(pin),
            'env'  : { },
            },
       }

# Run everything
run(times, warmup, runs(), workloads(), timeout, os.path.join(results_root,'dacapo'))
