#!/bin/bash

source paths.sh

mkdir $RESULTS_DIR

# Install python packages needed
sudo apt-get install -y --force-yes python-pip python-numpy python-matplotlib
sudo pip install monotonic

mkdir $CROCHET_CRIU_DIR
