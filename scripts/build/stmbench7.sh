#!/bin/bash

source ../paths.sh

# jvstm
sudo apt-get install -y --force-yes ant
git clone $JVSTM_REPO $JVSTM_DIR
pushd $JVSTM_DIR
{
    git checkout $JVSTM_BRANCH
    export JAVA_HOME=$JDK8_DIR
    mvn package -DskipTests
}
popd

# deuce
git clone $DEUCE_REPO $DEUCE_DIR
pushd $DEUCE_DIR
{
    git checkout $DEUCE_BRANCH
    export JAVA_HOME=$JDK7_DIR
    ant agent-jar
}
popd

# StmBench7
git clone $STMBENCH7_REPO $STMBENCH7_DIR
pushd $STMBENCH7_DIR/stmbench7
{
    git checkout $STMBENCH7_BRANCH
    ln -s `find $JVSTM_DIR/target -maxdepth 1 -name "jvstm*jar"` lib/jvstm.jar
    ln -s `find $DEUCE_DIR/bin -name "deuceAgent.jar"` lib/deuceAgent.jar
    ln -s `find $CROCHET_DIR/target -name "CRIJ-*SNAPSHOT.jar"` lib/crij.jar

    #JDK 7
    {
        export JAVA_HOME=$JDK7_DIR
        ant jar

        # Process the JDK7 rt.jar with Deuce
        export JAVA_HOME=$JDK7_DIR
        $JDK7_DIR/bin/java -Dorg.deuce.include=java.util.* -XX:-UseSplitVerifier -jar lib/deuceAgent.jar `find $JDK7_DIR -name rt.jar` dist/rt-instrumented.jar

        # Process the stmbench7 jar with Deuce
    $JDK7_DIR/bin/java -Dorg.deuce.include=java.util.* -XX:-UseSplitVerifier -jar lib/deuceAgent.jar dist/stmbench7-1.2.jar dist/stmbench7-1.2-instrumented.jar
    }

    #JDK 8
    {
        export JAVA_HOME=$JDK8_DIR
        rm -rf dist/stmbench7-1.2.jar classes
        ant jar
    }

}
popd
