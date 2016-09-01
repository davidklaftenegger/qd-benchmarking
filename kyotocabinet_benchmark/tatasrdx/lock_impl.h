#ifndef LOCK_IMPL_H
#define LOCK_IMPL_H

#define LOCK_TYPE_AgnosticRDXLock
#define LOCK_TYPE_WPRW_TATASLock

#define NZI_TYPE_ReaderGroups

extern "C" {
#include "lock_impl/utils/support_many_lock_types.h"
}

#endif // LOCK_IMPL_H
