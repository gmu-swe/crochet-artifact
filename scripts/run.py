#!/usr/bin/python2

import os
import subprocess
import datetime
import tempfile
import sys
from signal import SIGKILL
from monotonic import monotonic
from time import sleep

def doRun(run, run_name, args, out, time, timeout):

    for clean in args['clean']:
        with open('/dev/null', 'w') as devnull:
            subprocess.Popen(clean, stdout=devnull, stderr=devnull, shell=True)

    if 'bin' in args and args['bin'] is not '':
        bin = os.path.join(run['cmd'], args['bin'])
    else:
        bin = run['cmd']

    if 'vmargs' in args and args['vmargs'] is not '':
        if isinstance(args['vmargs'], dict):
            bin = bin.format(benchvmargs=args['vmargs'][run_name])
        else:
            bin = bin.format(benchvmargs=args['vmargs'])
    else:
        bin = bin.format(benchvmargs='')

    command = "{} {} {}".format(run['wrap'], bin, args['args'])
    if 'expect' in args:
        command = args['expect'].format(cmd=command, log=time)

    env = {}
    env.update(run['env'])
    env.update(args['env'])

    run_env = os.environ.copy()
    run_env.update(env)

    out.write(str(env)+"\n")

    server = None
    if 'server' in run and run['server'] is not '':
        out.write(run['server']+"\n")
        out.write(str(datetime.datetime.now())+"\n")
        out.write("\n\n\n")

        server = subprocess.Popen(run['server'], env=run_env,
                stdout=out, stderr=out, shell=True,
                preexec_fn=os.setsid)

        done = False
        while not done:
            with open(out.name, "r") as out2:
                lines = out2.readlines()
            for l in lines:
                if run["server-start"] in l:
                    done = True
                    break

    out.write(command+"\n")
    out.write(str(datetime.datetime.now())+"\n")
    out.write("\n\n\n")
    out.flush()

    start = monotonic()
    done = False

    while not done:
        if 'devnull' in run and run['devnull']:
            with open('/dev/null', 'w') as devnull:
                proc = subprocess.Popen(command, env=run_env,
                        stdout=devnull, stderr=out, shell=True,
                        preexec_fn=os.setsid)
        else:
            proc = subprocess.Popen(command, env=run_env,
                    stdout=out, stderr=out, shell=True,
                    preexec_fn=os.setsid)

        for t in range(0,timeout*4):
            sleep(0.25)
            if proc.poll() != None:
                done = True
                break

        if not done:
            os.killpg(os.getpgid(proc.pid), SIGKILL)
            proc.wait()
            with open('/dev/null', 'w') as devnull:
                proc = subprocess.Popen('killall -KILL vx',
                        stdout=devnull, stderr=devnull, shell=True,
                        preexec_fn=os.setsid)
            print("Retrying...")


    proc.wait()
    end = monotonic()

    if server is not None:
        os.killpg(os.getpgid(server.pid), SIGKILL)
        server.wait()


    if not 'expect' in args:
        with open(time, 'a') as time:
            time.write(str(end-start)+"\n")

def run(times, warmup, runs, commands, timeout, results_dir):
    for (name,comm) in commands.iteritems():

        for (run_name,run) in runs.iteritems():

            results = os.path.join(results_dir, name, run_name)
            if not os.path.exists(results):
                os.makedirs(results)

            for i in range(0,warmup):
                print("warm {} {} {} - {}".format(name, run_name, i, datetime.datetime.now()))
                with open('/dev/null', 'w') as devnull:
                    doRun(run, run_name, comm, devnull, '/dev/null', timeout)

            for i in range(0,times):
                print("run  {} {} {} - {}".format(name, run_name, i, datetime.datetime.now()))
                with open(os.path.join(results, 'out-{}.txt'.format(i)), 'w') as out:
                    time = os.path.join(results, 'res-{}.txt'.format(i))
                    doRun(run, run_name, comm, out, time, timeout)
