#!/usr/bin/python2

import os

def getenv(name):
    ret = os.environ[name]
    if ret is None:
        raise Exception('Could not find variable {} in environment (did you forget to `source paths.sh`?)'.format(name))

    return ret

# Where everything is installed
install_dir = getenv('INSTALL_DIR')

# Results directory
results_root = getenv('RESULTS_DIR')

# Generated charts directory
graphs_dir = getenv('GRAPHS_DIR')

# Generated tables directory
tables_dir = getenv('TABLES_DIR')

# jvstm
jvstmdir = getenv('JVSTM_DIR')

# stmbench7
stmbench7dir_jdk7 = getenv('STMBENCH7_JDK7_DIR')
stmbench7dir_jdk8 = getenv('STMBENCH7_JDK8_DIR')

# microbenchmarks
microbenchdir = getenv('MICROBENCH_DIR')

# deuce
deucedir = getenv('DEUCE_DIR')

# jdk7
jdk7dir = getenv('JDK7_DIR')

# jdk7
jdk8dir = getenv('JDK8_DIR')

# crochet
crochetdir = getenv('CROCHET_DIR')

dacapojar = getenv('DACAPO_JAR')

# metasploit
metasploitdir = getenv('METASPLOIT_DIR')

# crossftp
crossftpdir = getenv('CROSSFTP_DIR')

# dacapo-h2
dacapoh2dir = getenv('DACAPO_H2_DIR')

# global JVM args
globalJvmParams = getenv('GLOBAL_JVM_PARAMS')

# global JVM args
globalTimes = int(getenv('GLOBAL_TIMES'))
