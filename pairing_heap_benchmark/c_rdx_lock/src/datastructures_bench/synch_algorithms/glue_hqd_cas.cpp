#ifdef QUEUE_STATS
typedef union CacheLinePaddedBoolImpl {
    bool value;
    char padding[64];
} CacheLinePaddedBool;

typedef union CacheLinePaddedIntImpl {
    int value;
    char padding[128];
} CacheLinePaddedInt;


typedef union CacheLinePaddedULongImpl {
    unsigned long value;
    char padding[128];
} CacheLinePaddedULong;

typedef union CacheLinePaddedDoubleImpl {
    double value;
    char padding[128];
} CacheLinePaddedDouble;

typedef union CacheLinePaddedPointerImpl {
    void * value;
    char padding[64];
} CacheLinePaddedPointer;

extern __thread CacheLinePaddedULong helpSeasonsPerformed __attribute__((aligned(128)));
extern __thread CacheLinePaddedULong numberOfDeques __attribute__((aligned(128)));
#endif

#include "qd.hpp"

using intlock = mcs_lock;
using locktype = hqdlock_impl<intlock, intlock, dual_buffer_queue<6144, 24, atomic_instruction_policy_t::use_compare_and_swap>, pinning_policy_t::pinned_threads, starvation_policy_t::starvation_free>;

extern "C" {
#include "cpplock.h"
#include "cpplock.cpp"
} // extern "C"
