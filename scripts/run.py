#!/usr/bin/python2

import os
import subprocess
import datetime
import tempfile
import sys
from signal import SIGKILL
from monotonic import monotonic
from time import sleep

def doRun(run, args, out, time, timeout):
    if 'bin' in args and args['bin'] is not '':
        bin = os.path.join(run['cmd'], args['bin'])
    else:
        bin = run['cmd']

    command = "{} {} {}".format(run['wrap'], bin, args['args'])
    if 'expect' in args:
        command = args['expect'].format(cmd=command, log=time)

    env = {}
    env.update(run['env'])
    env.update(args['env'])

    out.write(str(env)+"\n")
    out.write(command+"\n")
    out.write(str(datetime.datetime.now())+"\n")
    out.write("\n\n\n")
    out.flush()

    run_env = os.environ.copy()
    run_env.update(env)

    start = monotonic()
    if 'devnull' in run and run['devnull']:
        with open('/dev/null', 'w') as devnull:
            proc = subprocess.Popen(command, env=run_env,
                    stdout=devnull, stderr=out, shell=True,
                    preexec_fn=os.setsid)
    else:
        proc = subprocess.Popen(command, env=run_env,
                stdout=out, stderr=out, shell=True,
                preexec_fn=os.setsid)

    proc.wait()
    end = monotonic()

    if not 'expect' in args:
        with open(time, 'a') as time:
            time.write(str(end-start)+"\n")

    for clean in args['clean']:
        with open('/dev/null', 'w') as devnull:
            subprocess.Popen(clean, stdout=devnull, stderr=devnull, shell=True)

def run(times, warmup, runs, commands, timeout, results_dir):
    for (name,comm) in commands.iteritems():

        for (run_name,run) in runs.iteritems():

            results = os.path.join(results_dir, name, run_name)
            if not os.path.exists(results):
                os.makedirs(results)

            for i in range(0,warmup):
                print("warm {} {} {} - {}".format(name, run_name, i, datetime.datetime.now()))
                with open('/dev/null', 'w') as devnull:
                    doRun(run, comm, devnull, '/dev/null', timeout)

            for i in range(0,times):
                print("run  {} {} {} - {}".format(name, run_name, i, datetime.datetime.now()))
                with open(os.path.join(results, 'out-{}.txt'.format(i)), 'w') as out:
                    time = os.path.join(results, 'res-{}.txt'.format(i))
                    doRun(run, comm, out, time, timeout)
