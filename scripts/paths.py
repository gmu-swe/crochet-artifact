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

# jvstm
jvstmdir = getenv('JVSTM_DIR')

# stmbench7
stmbench7dir = getenv('STMBENCH7_DIR')

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
