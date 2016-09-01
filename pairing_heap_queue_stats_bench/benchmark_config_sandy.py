#!/usr/bin/python

import sys
import os
import subprocess

bin_dir_path = os.path.dirname(os.path.realpath(__file__))

command = [
    os.path.join(bin_dir_path, 'benchmark_lock_XNonCW.py'),
    #number of iterations
    '5',
    #Output dir (standard menas a dir in bench_result based on the git
    #commit id and the date)
    'data_sandy',
    #benchmark prefixes (comma separated list)
    'pairing_heap_bench',
    #locks to benchmark (comma separated list)
    'cpp_qd,cpp_hqd,flatcomb,ccsynch,hsynch,oyamaopt',
    #use pinning to NUMA nodes (comma separated list)
    'no',
    #Benchmark number of threads (comma separated list)
    '64',
    #Procentage reads (comma separated list)
    '0.5',
    #Seconds to run the benchmark (comma separated list)
    '2',
    #Numper of work items performed in write-critical seciton (comma
    #separated list)
    '1',
    #Numper of work items performed in read-critical seciton (comma
    #separated list)
    '0',
    #Numper of work items performed in non-critical seciton (comma
    #separated list)
    '1,2,3,4,6,10,16,25,40,63,100,158,251,398,631,1000,1585,2512,3981']
 
process = subprocess.Popen(command)
process.wait()
