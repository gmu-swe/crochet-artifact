#!/bin/bash

source ../paths.sh

tar xvf `find $DOWNLOAD_DIR -maxdepth 1 -name "jdk-8*"` -C $INSTALL_DIR
mv `find $INSTALL_DIR -maxdepth 1 -name "jdk1.8*"` $JDK8_DIR

tar xvf `find $DOWNLOAD_DIR -maxdepth 1 -name "jdk-7*"` -C $INSTALL_DIR
mv `find $INSTALL_DIR -maxdepth 1 -name "jdk1.7*"` $JDK7_DIR

# Copy file from JDK8 to JDK7 for dacapo/eclipse benchmark to work
cp $JDK8_dir/jre/lib/tzdb.dat $JDK7_DIR/jre/lib
