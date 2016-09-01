#!/usr/bin/python

import sys
import os
import subprocess

bin_dir_path = os.path.dirname(os.path.realpath(__file__))

command = [
    os.path.join(bin_dir_path, 'benchmark_lock.py'),
    #number of iterations
    '5',
    #Output dir (standard menas a dir in bench_result based on the git
    #commit id and the date)
    'data_sandy',
    #benchmark prefixes (comma separated list)
    'rw_bench_clone',
    #locks to benchmark (comma separated list)
    'rcpp_hqd,drmcs_rgnzi,rcpp_qd,cohort,wprwcohort_rgnzi',
    #use pinning to NUMA nodes (comma separated list)
    'no',
    #Benchmark number of threads (comma separated list)
    '1,2,4,8,12,16,24,32,48,64',
    #Procentage reads (comma separated list)
    '0.5,0.8,0.95,0.99,1.0',
    #Seconds to run the benchmark (comma separated list)
    '2',
    #Numper of work items performed in write-critical seciton (comma
    #separated list)
    '4',
    #Numper of work items performed in read-critical seciton (comma
    #separated list)
    '4',
    #Numper of work items performed in non-critical seciton (comma
    #separated list)
    '0,32,128']
    #'0']

process = subprocess.Popen(command)
process.wait()
