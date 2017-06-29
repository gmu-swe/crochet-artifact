#!/bin/bash

source ../paths.sh

tar xvf `find $DOWNLOAD_DIR -maxdepth 1 -name "jdk-*"` -C $INSTALL_DIR
