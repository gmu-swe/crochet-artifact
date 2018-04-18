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
