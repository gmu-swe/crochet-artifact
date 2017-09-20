#!/bin/bash

source ../paths.sh

sudo apt-get install -y --force-yes maven build-essential
git clone $CROCHET_REPO $CROCHET_DIR
pushd $CROCHET_DIR
{
    git checkout $CROCHET_BRANCH
    export JAVA_HOME=`find $INSTALL_DIR -maxdepth 1 -name "jdk1.8*"`
    echo $JAVA_HOME
    mvn install -DskipTests
    ./instrumentJRE.sh
}
popd
