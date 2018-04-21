#!/usr/bin/bash


git clone git@github.com:gmu-swe/ClassChangeMicroBenchmarks.git

git clone git@github.com:gmu-swe/crochet.git

git clone git@github.com:gmu-swe/crossftp.git
pushd crossftp
{
    git checkout "crochet-1.07"
}
popd

git clone git@github.com:gmu-swe/dacapo-h2.git

git clone https://github.com/inesc-id-esw/jvstm.git

git clone https://github.com/gmu-swe/jvstm-benchmarks.git
pushd jvstm-benchmarks
{
    git checkout "checkpoint"
}
popd

git clone https://github.com/gmu-swe/DeuceSTM.git

git clone https://github.com/gmu-swe/metasploit-framework.git
pushd ftp-fuzz
{
    git checkout "ftp-fuzz"
}
popd

git clone https://github.com/gmu-swe/h2database.git
pushd h2database
{
    git checkout "release-1.2.121"
}
popd
