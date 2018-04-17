#!/bin/bash

source paths.sh

mkdir $INSTALL_DIR

pushd $BUILD_SCRIPTS_DIR
{
    ./jdk.sh
    ./crochet.sh
    ./dacapo-h2.sh
    ./micro.sh
    ./stmbench7.sh
    ./crossftp.sh
    #./xj.sh
}
popd
