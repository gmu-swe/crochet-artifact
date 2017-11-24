#!/bin/bash

source paths.sh

mkdir $INSTALL_DIR

pushd $BUILD_SCRIPTS_DIR
{
    ./jdk.sh
    ./crochet.sh
    ./micro.sh
    ./stmbench7.sh
    ./xj.sh
}
popd
