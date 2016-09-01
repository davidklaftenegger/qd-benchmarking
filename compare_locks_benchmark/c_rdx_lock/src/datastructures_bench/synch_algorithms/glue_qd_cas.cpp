#include "qd.hpp"

using intlock = mcs_futex_lock;
using locktype = qdlock_impl<intlock, dual_buffer_queue<6144, 16, atomic_instruction_policy_t::use_compare_and_swap>, starvation_policy_t::starvation_free>;

extern "C" {
#include "cpplock.h"
#include "cpplock.cpp"
} // extern "C"
