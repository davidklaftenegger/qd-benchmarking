#!/usr/bin/python

import sys
import os
import subprocess

bin_dir_path = os.path.dirname(os.path.realpath(__file__))

command = [
    os.path.join(bin_dir_path, 'benchmark_lock.py'),
    #number of iterations
    #'5',
    '5',
    #Output dir (standard menas a dir in bench_result based on the git
    #commit id and the date)
    'data_sandy',
    #benchmark prefixes (comma separated list)
    'pairing_heap_bench',
    #locks to benchmark (comma separated list)
    'cpp_tatas,cpp_qd,cpp_mcs,cpp_qd_nodetach,cpp_qd_cas,cohortlock,ccsynch,flatcomb,clh,lf,pthreadslock,oyamaopt,cpp_hqd,cpp_hqd_futex,cpp_hqd_cas,cpp_hqd_nodetach,cpp_hqd_starve,cpp_hqd_tatas,oyama,qdlock,hqdlock,hsynch',
    #use pinning to NUMA nodes (comma separated list)
    'no',
    #Benchmark number of threads (comma separated list)
    '1,2,3,4,5,6,7,8,12,16,24,32,48,64',
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
    '0,32,64,128']

process = subprocess.Popen(command)
process.wait()
