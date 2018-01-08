#!/usr/bin/python2

import sys
import os
import re
from os import listdir
from os.path import abspath
from os.path import join

import numpy

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

# Parser functions

def parse_file(path):

    error = True

    with open(path, 'r') as f:
        for line in f:
            if re.match('.*Invariants OK.$', line):
                error = False
                continue

            m = re.match('^Total throughput: (\d+\.\d+) op/s \((\d+\.\d+) op/s including failed\)$', line)
            if m is not None:
                if error:
                    print("File {} has errors, skipping results".format(path))
                    return None
                else:
                    return (float(m.group(1)), float(m.group(2)))

    print("File {} has no results or has errors, skipping".format(path))
    return None

def parse_results(paths):
    results = {}

    for arg in paths:
        for run in os.listdir(os.path.join(arg,'stmbench7')):
            for version in os.listdir(os.path.join(arg, 'stmbench7', run)):
                res = []
                for res_file in os.listdir(os.path.join(arg, 'stmbench7', run, version)):
                    if re.match('out-\d+\.txt', res_file):
                        f_res = parse_file(os.path.join(arg, 'stmbench7', run, version, res_file))
                        if f_res is not None:
                            (success,total) = f_res
                            res.append(success)
                results[version] = res

    return results

def average_stdev_results(results):
    ret = {}
    for (version,res) in results.iteritems():
        filtered = filter((lambda x: x is not None),res)
        ret[version] = (numpy.mean(filtered), numpy.std(filtered))

    return ret
