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

# CROCHET repo
export CROCHET_REPO=$ROOT/crochet
