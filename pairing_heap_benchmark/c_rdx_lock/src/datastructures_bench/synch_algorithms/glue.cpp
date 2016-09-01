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

using locktype = qdlock;

extern "C" {
#include "cpplock.h"

AgnosticDXLock* cpplock_new() {
	AgnosticDXLock* x = (AgnosticDXLock*) std::malloc(sizeof(AgnosticDXLock) + sizeof(locktype)-1+1024);
	new (&x->lock) locktype;
	return x;
}

void cpplock_init(AgnosticDXLock* x) {
	locktype* l = reinterpret_cast<locktype*>(&x->lock);
	new (l) locktype;
}
void cpplock_free(AgnosticDXLock* x) {
	locktype* l = reinterpret_cast<locktype*>(&x->lock);
	l->~locktype();
	std::free(x);
}
	
void cpplock_delegate(AgnosticDXLock* x, void (*delgateFun)(int, int *), int data) {
	locktype* l = reinterpret_cast<locktype*>(&x->lock);
	l->delegate_n([](void (*fun)(int, int *), int d) {fun(d, nullptr);}, delgateFun, data);
}
int cpplock_delegate_and_wait(AgnosticDXLock* x, void (*delgateFun)(int, int *), int data) {
	locktype* l = reinterpret_cast<locktype*>(&x->lock);
	int resp;
	std::atomic<bool> flag(false);
	l->delegate_n([](void (*fun)(int, int *), int d , int* r, std::atomic<bool>* f) { fun(d, r);  f->store(true, std::memory_order_release);}, delgateFun, data, &resp, &flag);
	while(!flag.load(std::memory_order_acquire)) {
		qd::pause();
	}
	return resp;
}
void cpplock_lock(AgnosticDXLock* x) {
	locktype* l = reinterpret_cast<locktype*>(&x->lock);
	l->lock();
}
void cpplock_unlock(AgnosticDXLock* x) {
	locktype* l = reinterpret_cast<locktype*>(&x->lock);
	l->unlock();
}

} // extern "C"
