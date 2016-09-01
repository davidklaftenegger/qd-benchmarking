#!/bin/bash

if [ ! -d c_rdx_lock ]
then
    cp -r ../pairing_heap_benchmark/c_rdx_lock .
fi

cd c_rdx_lock
scons --use_pinning --use_queue_stats
cd ..

HOSTNAME=`hostname`

DATADIR="data_$HOSTNAME"

cd c_rdx_lock

rm -r bench_results/

rm -r ../$DATADIR

if [ "$HOSTNAME" == "shome" ]
then
    cp ../benchmark_config_shome.py bin/benchmark_config_shome.py
    ./bin/benchmark_config_shome.py
elif [ "$HOSTNAME" == "sandy" ]
then
    cp ../benchmark_config_sandy.py bin/benchmark_config_sandy.py
    ./bin/benchmark_config_sandy.py
else
    echo "The hostname is not recognized. Modify run_benchmark.sh to fix the problem."
    exit 0
fi

mv bench_results/ ../$DATADIR
