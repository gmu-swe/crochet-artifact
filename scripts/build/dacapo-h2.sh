#!/bin/bash

source ../paths.sh

# H2
git clone $H2_REPO $H2_DIR
pushd $H2_DIR/h2
{
    git checkout $H2_BRANCH
    export JAVA_HOME=$JDK8_DIR
    ant jar
}
popd

# DaCapo
git clone $DACAPO_H2_REPO $DACAPO_H2_DIR
pushd $DACAPO_H2_DIR
{
    cp $H2_DIR/h2/bin/h2.jar benchmarks/libs/h2/downloads/h2-1.2.121.jar
    pushd benchmarks
    {
        ant h2
    }
}
popd
