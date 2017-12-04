#!/usr/bin/python2

import sys
import os

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

from run import run
from paths import *

# How many times should each run be repeated?
times = 1

# Number of warmup commands before starting to take measurements
warmup = 0

run_stmbench7_deuce="{jdk}/bin/java -Xbootclasspath:{stmbench7}/stmbench7/dist/rt-instrumented.jar:{deuce}/bin/deuceAgent.jar -Dorg.deuce.include=java.util.* -Dorg.deuce.transaction.contextClass={stm} -XX:-UseSplitVerifier {vmargs} -cp {stmbench7}/stmbench7/dist/stmbench7-1.2-instrumented.jar:{stmbench7}/stmbench7/lib/advice-runtime-1.8-SNAPSHOT.jar stmbench7.Benchmark {args}"

run_stmbench7_native="{jdk}/bin/java {vmargs} -cp {stmbench7}/stmbench7/dist/stmbench7-1.2.jar:{stmbench7}/stmbench7/lib/advice-runtime-1.8-SNAPSHOT.jar:{stmbench7}/stmbench7/lib/crij.jar:{stmbench7}/stmbench7/lib/jvstm.jar stmbench7.Benchmark {args}"

run_stmbench7_crochet="{crochet}/target/jre-inst/bin/java {vmargs} -agentpath:{crochet}/target/libtagging.so -javaagent:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -cp {stmbench7}/stmbench7/dist/stmbench7-1.2.jar:{stmbench7}/stmbench7/lib/advice-runtime-1.8-SNAPSHOT.jar:{stmbench7}/stmbench7/lib/crij.jar:{stmbench7}/stmbench7/lib/jvstm.jar stmbench7.Benchmark {args}"

# Git commands to try
def workloads() :
    return {
        'rw-no-traversals-10sec' : {
            'bin'   : '',
            'args'  : "-t 1 -l 10 -w rw --no-traversals",
            'clean' : [ ],
            'env'   : { }
            } ,
        }

vmargs="-Xmx4G"

# Max time any execution can take, in seconds
timeout = 3*60

def runs() :
    return {
        'native-nolock' : {
            'cmd'  : run_stmbench7_native.format(jdk=jdk8dir,
                stmbench7=stmbench7dir,
                vmargs="{} -DnoCheckpoint".format(vmargs),
                args="-g none"),
            'wrap' : '',
            'env'  : { },
            },
        'native-nolock-checkpoint' : {
            'cmd'  : run_stmbench7_native.format(jdk=jdk8dir,
                stmbench7=stmbench7dir,
                vmargs=vmargs,
                args="-g none"),
            'wrap' : '',
            'env'  : { },
            },
        'crochet-nolock' : {
            'cmd'  : run_stmbench7_crochet.format(
                crochet=crochetdir,
                stmbench7=stmbench7dir,
                vmargs="{} -DnoCheckpoint".format(vmargs),
                args="-g none"),
            'wrap' : '',
            'env'  : { },
            },
        'crochet-nolock-checkpoint' : {
            'cmd'  : run_stmbench7_crochet.format(
                crochet=crochetdir,
                stmbench7=stmbench7dir,
                vmargs="{}".format(vmargs),
                args="-g none"),
            'wrap' : '',
            'env'  : { },
            },
        'deuce-lsa'     : {
            'cmd'  : run_stmbench7_deuce.format(jdk=jdk7dir,
                stmbench7=stmbench7dir,
                deuce=deucedir,
                stm="org.deuce.transaction.lsa.Context",
                vmargs="{} -DnoCheckpoint".format(vmargs),
                args="-g stm -s stmbench7.impl.deucestm.DeuceSTMInitializer"),
            'wrap' : '',
            'env'  : { },
            },
        'deuce-lsa-checkpoint' : {
            'cmd'  : run_stmbench7_deuce.format(jdk=jdk7dir,
                stmbench7=stmbench7dir,
                deuce=deucedir,
                stm="org.deuce.transaction.lsa.Context",
                vmargs=vmargs,
                args="-g stm -s stmbench7.impl.deucestm.DeuceSTMInitializer"),
            'wrap' : '',
            'env'  : { },
            },
        'deuce-tl2'     : {
            'cmd'  : run_stmbench7_deuce.format(jdk=jdk7dir,
                stmbench7=stmbench7dir,
                deuce=deucedir,
                stm="org.deuce.transaction.tl2.Context",
                vmargs="{} -DnoCheckpoint".format(vmargs),
                args="-g stm -s stmbench7.impl.deucestm.DeuceSTMInitializer"),
            'wrap' : '',
            'env'  : { },
            },
        'deuce-tl2-checkpoint' : {
            'cmd'  : run_stmbench7_deuce.format(jdk=jdk7dir,
                stmbench7=stmbench7dir,
                deuce=deucedir,
                stm="org.deuce.transaction.tl2.Context",
                vmargs=vmargs,
                args="-g stm -s stmbench7.impl.deucestm.DeuceSTMInitializer"),
            'wrap' : '',
            'env'  : { },
            },
        'jvstm'     : {
            'cmd'  : run_stmbench7_native.format(jdk=jdk7dir,
                stmbench7=stmbench7dir,
                vmargs="{} -DnoCheckpoint".format(vmargs),
                args="-g stm -s stmbench7.impl.jvstm.JVSTMInitializer"),
            'wrap' : '',
            'env'  : { },
            },
        'jvstm-checkpoint' : {
            'cmd'  : run_stmbench7_native.format(jdk=jdk7dir,
                stmbench7=stmbench7dir,
                vmargs=vmargs,
                args="-g stm -s stmbench7.impl.jvstm.JVSTMInitializer"),
            'wrap' : '',
            'env'  : { },
            },
       }

# Run everything
run(times, warmup, runs(), workloads(), timeout, os.path.join(results_root,'stmbench7'))
