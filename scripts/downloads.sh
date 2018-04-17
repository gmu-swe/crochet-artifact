#!/bin/bash

source paths.sh

mkdir $DOWNLOAD_DIR
pushd $DOWNLOAD_DIR
{
    # JDK8
    # $WGET --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz
    # $WGET --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.tar.gz

    # Dacapo
    wget -nc -O $DACAPO_JAR https://sourceforge.net/projects/dacapobench/files/archive/9.12-bach/dacapo-9.12-bach.jar/download
}
popd
