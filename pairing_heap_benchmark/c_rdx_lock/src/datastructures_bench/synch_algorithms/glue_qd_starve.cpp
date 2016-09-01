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

using intlock = mcs_futex_lock;
using locktype = qdlock_impl<intlock, dual_buffer_queue<6144, 16, atomic_instruction_policy_t::use_fetch_and_add>, starvation_policy_t::may_starve>;

extern "C" {
#include "cpplock.h"
#include "cpplock.cpp"
} // extern "C"
