#!/bin/bash

source ../paths.sh

# CrossFTP
git clone $CROSSFTP_REPO $CROSSFTP_DIR
pushd $CROSSFTP_DIR
{
    git checkout $CROSSFTP_BRANCH
    ln -s $CROCHET_DIR/target/CRIJ-0.0.1-SNAPSHOT.jar common/lib/
    export JAVA_HOME=$JDK8_DIR
    ant dist
}

$ROOT/experiments/ftp/ftpd.properties.sh  > $CROSSFTP_DIR/ftpd.properties
$ROOT/experiments/ftp/users.properties.sh > $CROSSFTP_DIR/users.properties

# Fuzzer

# Deps
sudo apt-get install -y --force-yes libpq-dev libpcap-dev

# RVM/ruby/gems
curl -sSL https://rvm.io/mpapis.asc | gpg --import -
curl -sSL https://get.rvm.io | bash -s stable --ruby
source $HOME/.rvm/scripts/rvm
rvm install ruby-2.4.2
rvm --default use 2.4.2

# Metasploit
git clone $METASPLOIT_REPO $METASPLOIT_DIR
pushd $METASPLOIT_DIR
{
    git checkout $METASPLOIT_BRANCH
}
popd
gem install bundler
bundle install --gemfile=$METASPLOIT_DIR/Gemfile --system
