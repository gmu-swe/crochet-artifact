#!/bin/bash

# Root dir
ROOT=/vagrant

# Where everything is downloaded
export DOWNLOAD_DIR=$ROOT/downloads

# Where everything is installed
export INSTALL_DIR=/home/ubuntu/software

# Results directory
export RESULTS_DIR=$ROOT/results

# Generated charts directory
export GRAPHS_DIR=$ROOT/graphs

# Data directory
export DATA_DIR=$ROOT/data

# Patch directory
export PATCH_DIR=$ROOT/patches

# Build scripts directory
export BUILD_SCRIPTS_DIR=$ROOT/scripts/build

# wget command to download programs/data
WGET="$(which wget) -nc"

# JDKs
export JDK7_DIR=$INSTALL_DIR/jdk7
export JDK8_DIR=$INSTALL_DIR/jdk8
export OPENJDK_DIR=$INSTALL_DIR/openjdk

# CROCHET repo
export CROCHET_REPO=$ROOT/repos/crochet
export CROCHET_BRANCH=master
export CROCHET_DIR=$INSTALL_DIR/crochet

# Microbenchmark repo
export MICROBENCH_REPO=$ROOT/repos/ClassChangeMicroBenchmarks
export MICROBENCH_BRANCH=master
export MICROBENCH_DIR=$INSTALL_DIR/ClassChangeMicroBenchmarks

# STM stuff
export STMBENCH7_REPO=https://github.com/gmu-swe/jvstm-benchmarks.git
export STMBENCH7_BRANCH=checkpoint
export STMBENCH7_DIR=$INSTALL_DIR/stmbench7

export JVSTM_REPO=https://github.com/inesc-id-esw/jvstm.git
export JVSTM_BRANCH=master
export JVSTM_DIR=$INSTALL_DIR/jvstm

export DEUCE_REPO=https://github.com/gmu-swe/DeuceSTM.git
export DEUCE_BRANCH=master
export DEUCE_DIR=$INSTALL_DIR/deuce

# CRIU dir to dump the checkpoints
export CROCHET_CRIU_DIR=/home/ubuntu/criu-dump

export DACAPO_JAR=$ROOT/dacapo-9.12-bach.jar

# CROSSFTP repo
export CROSSFTP_REPO=$ROOT/repos/crossftp
export CROSSFTP_BRANCH=crochet-1.07
export CROSSFTP_DIR=$INSTALL_DIR/crossftp

# METASPLOIT repo
export METASPLOIT_REPO=https://github.com/gmu-swe/metasploit-framework.git
export METASPLOIT_BRANCH=ftp-fuzz
export METASPLOIT_DIR=$INSTALL_DIR/metasploit

# H2 repo
export H2_REPO=https://github.com/gmu-swe/h2database.git
export H2_BRANCH=release-1.2.121
export H2_DIR=$INSTALL_DIR/h2

# DaCapo H2 repo
export DACAPO_H2_REPO=$ROOT/repos/dacapo-h2
export DACAPO_H2_BRANCH=master
export DACAPO_H2_DIR=$INSTALL_DIR/dacapo-h2
