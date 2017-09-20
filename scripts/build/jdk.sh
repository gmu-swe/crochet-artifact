#!/bin/bash

source ../paths.sh

tar xvf `find $ROOT -maxdepth 1 -name "jdk-8*"` -C $INSTALL_DIR
mv `find $INSTALL_DIR -maxdepth 1 -name "jdk1.8*"` $JDK8_DIR

tar xvf `find $ROOT -maxdepth 1 -name "jdk-7*"` -C $INSTALL_DIR
mv `find $INSTALL_DIR -maxdepth 1 -name "jdk1.7*"` $JDK7_DIR
