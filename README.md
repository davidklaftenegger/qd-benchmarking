# qd-benchmarking
Queue Delegation Locking benchmarking codes

The main queue delegation lock implementation is in the directory `qd_library`

The directory `pairing_heap_benchmark` contains the priority queue benchmark,
it can be started through [`run_benchmark.sh`](pairing_heap_benchmark/run_benchmark.sh), but first a configuration has to be adjusted.
An example for our testing machine can be found in [`benchmark_config_sandy.py`](pairing_heap_benchmark/benchmark_config_sandy.py).
Adjust `run_benchmark.sh` as needed for your system.


The directory `pairing_heap_queue_stats_bench` contains a setup for measuring the number of operations per help session.
It will copy the `c_rdx_lock` directory from the above benchmark, so make sure this is clean.
An example configuration can again be found in [`benchmark_config_sandy.py`](pairing_heap_queue_stats_bench/benchmark_config_sandy.py) and the script is again [`run_benchmark.sh`](pairing_heap_queue_stats_bench/run_benchmark.sh)

The directory `compare_locks_benchmark` contains the code for the readers-writer lock benchmark.
Again, configuration [`benchmark_config_sandy.py`](compare_locks_benchmark/benchmark_config_sandy.py) and [`run_benchmark.sh`](compare_locks_benchmark/run_benchmark.sh) need to be adjusted.

Each directory contains example python scripts for how to create graphs out of the resulting data files.
These need to be manually adjusted to fit the benchmark configuration at hand.
In all three of the above benchmarks, the created binaries contain the following names (which are also used in the configuration) to denote which lock is used:
 - QD lock -> cpp_qd
 - HQD lock -> cpp_hqd
 - Flat Combining -> flatcomb [1]
 - CC-Synch -> ccsynch [2]
 - H-Synch -> hsynch [2]
 - DetachExec -> oyamaopt (optimization by us, based on [2])
 - Lock-free priority queue by Lindén and Jonsson -> lf [3]
 - Pthreads -> pthreadslock
 - CLH lock -> clh [2]
 - Cohort lock -> cohortlock (see [4] for algorithm)
 - MR-QD -> rcpp_qd 
 - MR-HQD -> rcpp_hqd
 - DR-MCS -> drmcs_rgnzi (see [5] for algorithm)
 - WPRW-Cohort -> wprwcohort_rgnzi (see [5] for algorithm)

[1] https://github.com/mit-carbon/Flat-Combining

[2] https://github.com/nkallima/sim-universal-construction

[3] https://link.springer.com/chapter/10.1007%2F978-3-319-03850-6_15 - code provided by authors

[4] https://dl.acm.org/citation.cfm?id=2145848

[5] https://dl.acm.org/citation.cfm?id=2442532



The directory `kyotocabinet-1.2.76` contains an unchanged kyoto cabinet sourcecode, which allows measuring their Pthreads implementation.

The directory `kyotocabinet_benchmark` contains our modified version of the kyoto cabinet using different locking algorithms

The directory `kyotocabinet_interleaved` contains our modified version of the kyoto cabinet that also allows limited detached execution.

For running our versions of kyotocabinet, you must change the code that defines the `NUMBER_OF_NUMA_NODES`, `NUMBER_OF_CPUS_PER_NODE`, and `NUMA_STRUCTURE` according to your system in
[`lock_impl.h`](kyotocabinet_benchmark/lock_impl.h) and [`lock_impl.h`](kyotocabinet_interleaved/lock_impl.h).

To find your NUMA structure, it may be helpful to look at [`pairing_heap_benchmark/c_rdx_lock/src/lock/extract_numa_structure.py`](pairing_heap_benchmark/c_rdx_lock/src/lock/extract_numa_structure.py).

To run the kyotocabinet benchmarks follow the instructions in the subdirectory [`README.md`](kyotocabinet_benchmark/)
