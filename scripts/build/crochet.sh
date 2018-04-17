#!/bin/bash

source ../paths.sh

sudo apt-get install -y --force-yes maven build-essential criu
git clone $CROCHET_REPO $CROCHET_DIR
pushd $CROCHET_DIR
{
    git checkout $CROCHET_BRANCH
    export JAVA_HOME=$JDK8_DIR
    mvn install -DskipTests
    ./instrumentJRE.sh
    make libcriu.dylib

    # Get JCE from Openjdk8 and instrument it
    rm $CROCHET_DIR/target/jre-inst/jre/lib/jce.jar
    $JDK8_DIR/bin/java -Xmx6g -jar $CROCHET_DIR/target/CRIJ-0.0.1-SNAPSHOT.jar /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/jce.jar $CROCHET_DIR/target/jre-inst/jre/lib/

}
popd
