#ifndef LOCK_IMPL_SWITCHABLE_H
#define LOCK_IMPL_SWITCHABLE_H

/**********************************************************/
/* example: system with four Intel(R) Xeon(R) CPU E5-4650s processors, totalling 32 cores / 64 threads */
/* number of NUMA nodes (a.k.a. sockets, processor chips) in the system */
#define NUMBER_OF_NUMA_NODES 4 

/* number of logical cpus (a.k.a. hardware threads) per NUMA node */
#define NUMBER_OF_CPUS_PER_NODE 16 

/* the structure of the system */
#define NUMA_STRUCTURE {{0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60},{1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61},{2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62},{3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63}} 

/* another example: system with one Intel(R) Core(TM) i7-3770 CPU (4 cores / 8 threads) */
// #define NUMBER_OF_NUMA_NODES 1
// #define NUMBER_OF_CPUS_PER_NODE 8
// #define NUMA_STRUCTURE {{0,1,2,3,4,5,6,7}}

/**********************************************************/

#define NUMBER_OF_HARDWARE_THREADS ((NUMBER_OF_NUMA_NODES)*(NUMBER_OF_CPUS_PER_NODE))
#define ARRAY_SIZE NUMBER_OF_HARDWARE_THREADS
#define NUMBER_OF_READER_GROUPS NUMBER_OF_HARDWARE_THREADS

/* include currently set lock header */
#ifndef INCLUDE_NO_LOCK
#include "lock/lock_impl.h"
#endif

#endif
