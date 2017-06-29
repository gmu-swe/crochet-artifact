#!/bin/bash

source paths.sh

mkdir $DOWNLOAD_DIR
pushd $DOWNLOAD_DIR
{
    # JDK8
    echo $WGET
    $WGET --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz

}
popd
