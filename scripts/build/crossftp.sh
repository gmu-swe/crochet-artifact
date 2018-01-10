#!/bin/bash

source ../paths.sh

# Deps
sudo apt-get install -y --force-yes libpq-dev libpcap-dev

# CrossFTP
git clone $CROSSFTP_REPO $CROSSFTP_DIR
pushd $CROSSFTP_DIR
{
    git checkout $CROSSFTP_BRANCH
    ln -s $CROCHET_DIR/target/CRIJ-0.0.1-SNAPSHOT.jar common/lib/
    export JAVA_HOME=$JDK8_DIR
    ant dist
}

# Fuzzer

# RVM/ruby/gems
curl -sSL https://rvm.io/mpapis.asc | gpg --import -
curl -sSL https://get.rvm.io | bash -s stable --ruby
source /home/ubuntu/.rvm/scripts/rvm
rvm install ruby-2.4.2
gem install bundler

# Metasploit
git clone $METASPLOIT_REPO $METASPLOIT_DIR
pushd $METASPLOIT_DIR
{
    git checkout $METASPLOIT_BRANCH
    pushd metasploit-framework
    {
        bundle install
    }
    popd
}
popd
