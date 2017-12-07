#!/bin/bash

source ../paths.sh

sudo apt-get install -y --force-yes maven build-essential
git clone $CROCHET_REPO $CROCHET_DIR
pushd $CROCHET_DIR
{
    git checkout $CROCHET_BRANCH
    export JAVA_HOME=$JDK8_DIR
    echo $JAVA_HOME
    mvn install -DskipTests
    ./instrumentJRE.sh
    make libcriu.dylib
}
popd
