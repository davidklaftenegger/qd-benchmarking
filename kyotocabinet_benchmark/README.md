Kyoto Cabinet lock benchmarking
===============================

This folder contains a patched version of the Kyoto Cabinet, which can be
obtained unpatched here:
http://fallabs.com/kyotocabinet/pkg/kyotocabinet-1.2.76.tar.gz

To build this patched version you need to make sure that
 * lock_bin is a symlink to the lock implementation bin directory
   and contains the required object files (built with --use_pinning)
 * lock_impl is a symlink to the corresponding src directory
 * lock is a symlink to the locking implementation you wish to use

The choices for locking implementations are
 - drmcs     (DR-MCS lock)
 - numarw    (WPRW-Cohort lock)
 - tatasrdx  (MR-QD lock)
 - rhqd      (MR-HQD lock)


Before you compile, make sure you change the definition of
NUMBER_OF_NUMA_NODES
NUMBER_OF_CPUS_PER_NODE
NUMA_STRUCTURE
to match your testing environment.
in lock_impl.h

Note that lock is a symlink to the currently chosen locktype.
The corresponing subfolder contains a lock_impl.h specialization
which is included by the main lock_impl.h


You can use the following command to rebuild with a different lock:
rm lock ; ln -s $locktype lock ; make clean ; make -j

To run the kccachetest benchmark, run:
LD_LIBRARY_PATH=. ./kccachetest wicked -th $threads 100000 | grep time
