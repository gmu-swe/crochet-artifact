#!/usr/bin/python2

import sys
import os
import re
from os import listdir
from os.path import abspath
from os.path import join

from parse import parse_results,average_stdev_results

scripts_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../../scripts'))
os.sys.path.insert(0, scripts_dir)

results   = parse_results(sys.argv[1:])

processed = average_stdev_results(results)

len_version = 0

for (version,(avg,std)) in processed.iteritems():
    len_version = max(len_version, len(version))

order = [
        ("native-nolock-jdk7",        "native-nolock-jdk7"),
        ("native-nolock-jdk8",        "native-nolock-jdk8"),
        ("crochet-nolock",            "crochet-nolock"),
        ("crochet-nolock-checkpoint", "crochet-nolock-checkpoint"),
        ("deuce-tl2",                 "deuce-tl2"),
        ("deuce-tl2-notx",            "deuce-tl2-notx"),
        ("deuce-tl2-checkpoint",      "deuce-tl2-checkpoint"),
        ("deuce-lsa",                 "deuce-lsa"),
        ("deuce-lsa-notx",            "deuce-lsa-notx"),
        ("deuce-lsa-checkpoint",      "deuce-lsa-checkpoint"),
        ("jvstm",                     "jvstm"),
        ("jvstm-notx",                "jvstm-notx"),
        ("jvstm-checkpoint",          "jvstm-checkpoint"),
        ]

for (version,rename) in order:
    (avg,std) = processed[version]
    print("{:{a}{w}} & {:8.2f} \\pm {:8.2f} \\\\".format(rename,avg,std,a='<',w=len_version))

print("\n\n")

for (version,(avg,std)) in processed.iteritems():
    print("{:{a}{w}} & {:8.2f} \\pm {:8.2f} \\\\".format(version,avg,std,a='<',w=len_version))
