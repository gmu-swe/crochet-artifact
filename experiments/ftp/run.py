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

metasploit_setup = '\
"use auxiliary/fuzzers/ftp/ftp_pre_post;\
set DELAY 0;\
set STARTATSTAGE 4;\
set RHOSTS "127.0.0.1";\
set RPORT 5555;\
set USER user;\
set PASS pass;\
'

metasploit_setup_restart = metasploit_setup + '\
set SERVERCMD \\"{servercmd}\\";\
set SERVERUP \\"Server ready :: CrossFTP Server\\";\
'

metasploit_setup_crochet = metasploit_setup_restart + '\
set SIGNAL USR2;\
'

metasploit_run = '\
set ENDSIZE {end};\
info;\
run;\
quit\
"'

vmargs="{}".format(globalJvmParams)

native_server= "{jdk}/bin/java {vmargs} -cp {crossftpdir}/common/lib/commons-logging-1.0.3.jar:{crossftpdir}/common/lib/CRIJ-0.0.1-SNAPSHOT.jar:{crossftpdir}/common/lib/jnlp-1.0.jar:{crossftpdir}/common/lib/jnlp.jar:{crossftpdir}/common/lib/log4j-1.2.12.jar:{crossftpdir}/common/lib/README.txt:{crossftpdir}/dist/crossftp-1.07.jar org.apache.ftpserver.commandline.CommandLine -prop {crossftpdir}/ftpd.properties".format(vmargs=vmargs,jdk=jdk8dir,crossftpdir=crossftpdir)

crochet_server="{crochet}/target/jre-inst/bin/java {vmargs} {{opt}} -agentpath:{crochet}/target/libtagging.so -javaagent:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -Xbootclasspath/p:{crochet}/target/CRIJ-0.0.1-SNAPSHOT.jar -cp {crossftpdir}/common/lib/commons-logging-1.0.3.jar:{crossftpdir}/common/lib/CRIJ-0.0.1-SNAPSHOT.jar:{crossftpdir}/common/lib/jnlp-1.0.jar:{crossftpdir}/common/lib/jnlp.jar:{crossftpdir}/common/lib/log4j-1.2.12.jar:{crossftpdir}/common/lib/README.txt:{crossftpdir}/dist/crossftp-1.07.jar org.apache.ftpserver.commandline.CommandLine -prop {crossftpdir}/ftpd.properties".format(vmargs=vmargs,crochet=crochetdir,crossftpdir=crossftpdir)

run_native="{metasploit}/msfconsole -x"

def workloads() :
    return {
        'quick' : {
            'args'  : metasploit_run.format(end=20),
            'clean' : [ ],
            'env'   : { }
            } ,
        }

# Max time any execution can take, in seconds
timeout = 30*60

pin='numactl --membind 1 --cpunodebind 1' # eg 'taskset -c 5,6,7'

def runs() :
    return {
        'native' : {
            'server' : native_server,
            'server-start': "Server ready :: CrossFTP Server",
            'cmd'  : '{}/msfconsole -x {}'.format(metasploitdir,metasploit_setup),
            'wrap' : '{} /usr/bin/time'.format(pin),
            'env'  : { },
            },
        'restart' : {
            'cmd'  : '{}/msfconsole -x {}'.format(metasploitdir,metasploit_setup_restart.format(servercmd=native_server)),
            'wrap' : '{} /usr/bin/time'.format(pin),
            'env'  : { },
            },
        'crochet-baseline' : {
            'server' : crochet_server.format(opt=""),
            'server-start': "Server ready :: CrossFTP Server",
            'cmd'  : '{}/msfconsole -x {}'.format(metasploitdir,metasploit_setup),
            'wrap' : '{} /usr/bin/time'.format(pin),
            'env'  : { },
            },
        'crochet' : {
            'cmd'  : '{}/msfconsole -x {}'.format(metasploitdir,metasploit_setup_crochet.format(servercmd=crochet_server.format(opt="-Dcrochet"))),
            'wrap' : '{} /usr/bin/time'.format(pin),
            'env'  : { },
            },
       }

# Run everything
run(times, warmup, runs(), workloads(), timeout, os.path.join(results_root,'ftp'))
