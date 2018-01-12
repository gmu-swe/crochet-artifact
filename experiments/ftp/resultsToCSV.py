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

    with open(path, 'r') as f:
        for line in f:
            if re.match('java.lang.NullPointerException', line):
                break
            m = re.match('.*m(\d+\.\d+)user (\d+.\d+)system (\d+:\d+\.\d+)elapsed', line)
            if m is not None:
                ret = {}
                ret['user']    = m.group(1)
                ret['system']  = m.group(2)
                ret['elapsed'] = m.group(3)
                return ret

    print("File {} has no results or has errors, skipping".format(path))
    return None

def parse_results(paths):
    results = {}

    for arg in paths:
        for run in os.listdir(os.path.join(arg,'ftp')):
            for version in os.listdir(os.path.join(arg, 'ftp', run)):
                res = []
                for res_file in os.listdir(os.path.join(arg, 'ftp', run, version)):
                    if re.match('out-\d+\.txt', res_file):
                        f_res = parse_file(os.path.join(arg, 'ftp', run, version, res_file))
                        if f_res is not None:
                            res.append(f_res)
                results[version] = res

    return results

def resultsToCSV(results):
    print("config,user,system,elapsed")
    for (c,rs) in results.iteritems():
        for r in rs:
            print(c + ",{user},{system},{elapsed}".format(**r))


results   = parse_results(sys.argv[1:])
resultsToCSV(results)
