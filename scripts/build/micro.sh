#!/bin/bash

source ../paths.sh

sudo apt-get install criu

git clone $MICROBENCH_REPO $MICROBENCH_DIR
pushd $MICROBENCH_DIR
{
    git checkout $MICROBENCH_BRANCH
    export JAVA_HOME=$JDK8_DIR
    mvn package -DskipTests
}
popd
