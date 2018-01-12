#!/usr/bin/python2

import sys
import re

def before_stats(line,results):
    if re.match('^-*$', line):
        return stats_banner_1
    else:
        return before_stats

def stats_banner_1(line,results):
    if re.match('Benchmark statistics', line):
        return stats_banner_2
    else:
        return before_stats

def stats_banner_2(line,results):
    if re.match('^-*$', line):
        return stats_avg_length
    else:
        return before_stats

def stats_avg_length(line,results):
    assert(re.match('\s+Average traversal length:\s+NaN', line))
    return stats_struct_mod

def stats_struct_mod(line,results):
    assert(re.match('\s+Struct Modifications:\s+0', line))
    return stats_throughput_prev

def stats_throughput_prev(line,results):
    m = re.match('\s+Previous throughput \(ops/s\):\s+(\d+\.\d+)', line)
    assert(m)
    results['building'] = {}
    results['building']['prev'] = m.group(1)
    return stats_throughput_new

def stats_throughput_new(line,results):
    m = re.match('\s+New throughput \(ops/s\):\s+(\d+\.\d+)', line)
    assert(m)
    results['building']['new'] = m.group(1)
    return stats_total_time

def stats_total_time(line,results):
    m = re.match('\s+Total elapsed time \(s\):\s+(\d+\.\d+)', line)
    assert(m)
    results['building']['total'] = m.group(1)
    return stats_time

def stats_time(line,results):
    m = re.match('\s+Elapsed time \(s\):\s+(\d+\.\d+)', line)
    assert(m)
    results['building']['time'] = m.group(1)
    return stats_total_ops

def stats_total_ops(line,results):
    m = re.match('\s+Total operations:\s+(\d+\.\d+)\s+\( 100 %\)', line)
    assert(m)
    results['building']['ops'] = m.group(1)

    if 'complete' not in results:
        results['complete'] = []

    results['complete'].append(results['building'])
    return before_stats

def parse_file(path):

    results = {}
    func    = before_stats

    with open(path, 'r') as f:
        for line in f:
            func = func(line, results)

    return results['complete']

def parse_results(paths):
    results = {}

    for res_file in paths:
        f_res = parse_file(res_file)
        if f_res is not None:
            results[res_file] = f_res

    return results

def results_to_csv(res):
    print("config, prev_throughput, new_throughput, total_time, time, ops")
    for (config, results) in res.iteritems():
        for r in results:
            print(config + (", {prev}, {new}, {total}, {time}, {ops}".format(**r)))


results_to_csv(parse_results(sys.argv[1:]))
