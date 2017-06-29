#!/bin/bash

source ../paths.sh

sudo apt-get install -y --force-yes maven build-essential
git clone $CROCHET_REPO $INSTALL_DIR/crochet
pushd `find $INSTALL_DIR -maxdepth 1 -name "*crochet*"`
{
    export JAVA_HOME=`find $INSTALL_DIR -maxdepth 1 -name "jdk*"`
    mvn install -DskipTests
    ./instrumentJRE.sh
}
popd
