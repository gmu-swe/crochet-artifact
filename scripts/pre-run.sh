#!/bin/bash

source paths.sh

# Install python packages needed
sudo apt-get install -y python-monotonic

# Create directories to be populated later
mkdir $CROCHET_CRIU_DIR
mkdir $RESULTS_DIR
mkdir $TABLES_DIR

# Install R
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo add-apt-repository 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial/'
sudo apt-get update
sudo apt-get install -y r-base
sudo R -e 'install.packages(c("readr","mratios"))'
