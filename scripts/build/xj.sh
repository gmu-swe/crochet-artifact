#!/bin/bash

source ../paths.sh

sudo apt-get install zip unzip libfreetype6-dev libcups2-dev libasound2-dev libx11-dev libxt-dev libxaw7-dev libxtst-dev libxrender-dev

unzip "$ROOT/openjdk.zip" -d $INSTALL_DIR
pushd $OPENJDK_DIR
{
    unset JAVA_HOME
    export LANG=C
    export ARCH_DATA_MODEL=64
    export ALT_BOOTDIR=$JDK7_DIR
    export DISABLE_HOTSPOT_OS_VERSION_CHEDK=ok
    patch -p1 < $PATCH_DIR/hotspot-Makefile.patch
    patch -p1 < $PATCH_DIR/jmxstubs-Makefile.patch
    make all
}
popd

unzip "$ROOT/xj.zip" -d $INSTALL_DIR
pushd $INSTALL_DIR/ASM-5.0.3
{
    export JAVA_HOME=$JDK7_DIR
    ant jar
}
popd

pushd $INSTALL_DIR/transform
{
    export JAVA_HOME=$JDK7_DIR
    ant
}
popd

pushd $INSTALL_DIR/xjrt
{
    export JAVA_HOME=$JDK7_DIR
    ant
    ant # yeah, twice does it
}
popd

pushd $INSTALL_DIR/xj_collections
{
    export JAVA_HOME=$JDK7_DIR
    ant
}
popd

pushd $INSTALL_DIR/xjc
{
    export JAVA_HOME=$JDK7_DIR
    ant
}

pushd $INSTALL_DIR/xjopt
{
    export JAVA_HOME=$JDK7_DIR
    ant
}

pushd $INSTALL_DIR/ruggedj
{
    export JAVA_HOME=$JDK7_DIR
    ant
    pushd Benchmarks/synchroBench
    {
        patch -p1 < synchrobench.patch
        PATH=$JDK7_DIR/bin:$PATH ant
        sh preprocess.sh
    }
    popd
}
popd
