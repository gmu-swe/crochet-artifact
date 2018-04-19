#!/bin/bash

source ../paths.sh

sudo yum -y install zip unzip freetype-devel cups-devel cups-libs alsa-lib-devel ant libstdc++-static libX11-devel libXt-devel libXext-devel libXrender-devel libXtst-devel

sudo timedatectl set-ntp 0
sudo timedatectl set-time "2017-07-01 00:00:00"
unzip "$DOWNLOAD_DIR/openjdk.zip" -d $INSTALL_DIR
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
sudo timedatectl set-ntp 1

unzip "$DOWNLOAD_DIR/xj.zip" -d $INSTALL_DIR
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

    sed -i "s#/etc/alternatives/java_sdk_1.7.0#$JDK7_DIR#g" Makefile
    make
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
    pushd jvmti_agent
    {
        mkdir obj
        #patch -p1 < $PATCH_DIR/jvmti_agent_Makefile.patch
        sed -i "s#/etc/alternatives/java_sdk_1.7.0#$JDK7_DIR#g" Makefile
        export JAVA_HOME=$JDK7_DIR
        make
    }
    popd

    mv Benchmarks/synchroBench Benchmarks/synchroBench.bak
    git clone $SYNCHROBENCH_REPO Benchmarks/synchroBench
    pushd Benchmarks/synchroBench
    {
        sed -i "s#/home/tguest/crochet-artifact/software/crochet#$CROCHET_DIR#g" build.xml
        patch -p1 < $PATCH_DIR/synchrobench.patch
        PATH=$JDK7_DIR/bin:$PATH ant
        PATH=$JDK7_DIR/bin:$PATH bash preprocess.sh
    }
    popd
}
popd
