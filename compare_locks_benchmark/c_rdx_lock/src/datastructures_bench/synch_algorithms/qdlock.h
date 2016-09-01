
#ifndef QDLOCK_H
#define QDLOCK_H

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <limits.h>
#include <stdio.h>
#include <limits.h>


#ifndef SMP_UTILS_H
#define SMP_UTILS_H

//SMP Utils

//Make sure compiler does not optimize away memory access
#define ACCESS_ONCE(x) (*(volatile typeof(x) *)&(x))

//Atomic get
#define GET(value_ptr)  __sync_fetch_and_add(value_ptr, 0)

//Compiller barrier
#define barrier() __asm__ __volatile__("": : :"memory")

//See the following URL for explanation of acquire and release semantics:
//http://preshing.com/20120913/acquire-and-release-semantics

//Load with acquire barrier
#if __x86_64__
#define load_acq(assign_to,load_from) \
    assign_to = ACCESS_ONCE(load_from)
#else
#define load_acq(assign_to,load_from)           \
    do {                                        \
        barrier();                              \
        assign_to = ACCESS_ONCE(load_from);     \
        __sync_synchronize();                   \
    } while(0)
#endif


//Store with release barrier
#if __x86_64__
#define store_rel(store_to,store_value) \
    do{                                 \
        barrier();                      \
        store_to = store_value;        \
        barrier();                      \
    }while(0);
#else
#define store_rel(store_to,store_value) \
    do{                                 \
        __sync_synchronize();           \
        store_to = store_value;        \
        barrier();                      \
    }while(0);
#endif

//Intel pause instruction
#if __x86_64__
#define pause_instruction() \
  __asm volatile ("pause")
#else
#define pause_instruction() \
  __sync_synchronize()
#endif

static inline
int get_and_set_int(int * pointerToOldValue, int newValue){
    int x = ACCESS_ONCE(*pointerToOldValue);
    while (true) {
        if (__sync_bool_compare_and_swap(pointerToOldValue, x, newValue))
            return x;
        x = ACCESS_ONCE(*pointerToOldValue);
    }
}

static inline
unsigned long get_and_set_ulong(unsigned long * pointerToOldValue, unsigned long newValue){
    unsigned long x = ACCESS_ONCE(*pointerToOldValue);
    while (true) {
        if (__sync_bool_compare_and_swap(pointerToOldValue, x, newValue))
            return x;
        x = ACCESS_ONCE(*pointerToOldValue);
    }
}

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

#endif

//TATAS Lock

typedef struct TATASLockImpl {
    char pad1[64];
    void (*writer)(int, int *);
    char pad2[64 - sizeof(void (*)(void*)) % 64];
    char pad3[64];
    CacheLinePaddedBool lockWord;
    char pad4[64];
} TATASLock;


static inline
void tataslock_initialize(TATASLock * lock, void (*writer)(int, int *)){
    lock->writer = writer;
    lock->lockWord.value = 0;
    __sync_synchronize();
}

static inline
void tataslock_free(TATASLock * lock){
    free(lock);
}

static inline
void tataslock_register_this_thread(){
}

static inline
void tataslock_write_read_lock(TATASLock *lock);
static inline
void tataslock_write_read_unlock(TATASLock * lock);
static inline
void tataslock_write(TATASLock *lock, int writeInfo) {
    tataslock_write_read_lock(lock);
    lock->writer(writeInfo, 0);
    tataslock_write_read_unlock(lock);
}

static inline
void tataslock_write_read_lock(TATASLock *lock) {
    bool currentlylocked;
    while(true){
        load_acq(currentlylocked, lock->lockWord.value);
        while(currentlylocked){
            load_acq(currentlylocked, lock->lockWord.value);
        }
        currentlylocked = __sync_lock_test_and_set(&lock->lockWord.value, true);
        if(!currentlylocked){
            //Was not locked before operation
            return;
        }
        __sync_synchronize();//Pause instruction?
    }
}

static inline
void tataslock_write_read_unlock(TATASLock * lock) {
    __sync_lock_release(&lock->lockWord.value);
}

static inline
void tataslock_read_lock(TATASLock *lock) {
    tataslock_write_read_lock(lock);
}

static inline
void tataslock_read_unlock(TATASLock *lock) {
    tataslock_write_read_unlock(lock);
}


static inline
bool tataslock_is_locked(TATASLock *lock){
    bool locked;
    load_acq(locked, lock->lockWord.value);
    return locked;
}

static inline
bool tataslock_try_write_read_lock(TATASLock *lock) {
    //return __sync_bool_compare_and_swap(&lock->lockWord.value, false, true);
    return !__sync_lock_test_and_set(&lock->lockWord.value, true);
}

//Multi write queue

#define MWQ_CAPACITY MAX_NUM_OF_HELPED_OPS

#define PAD_QUEUE_ELEMENTS_TO_TWO_CACHE_LINES
typedef struct DelegateRequestEntryImpl {
    void (*request)(int, int*);
    int data;
    int * responseLocation;
#ifdef PAD_QUEUE_ELEMENTS_TO_TWO_CACHE_LINES
    char pad[128 - ((2*sizeof(void *)) + sizeof(int))];
#endif
} DelegateRequestEntry;

typedef struct DRMWQImpl {
    char padd1[64];
    CacheLinePaddedBool closed;
    char padd2[64];
    CacheLinePaddedULong elementCount;
    DelegateRequestEntry elements[MWQ_CAPACITY];
    char padd3[64 - ((sizeof(DelegateRequestEntry)*MWQ_CAPACITY) % 64)];
} DRMWQueue;

static DRMWQueue * drmvqueue_create();
static DRMWQueue * drmvqueue_initialize(DRMWQueue * queue);
static void drmvqueue_free(DRMWQueue * queue);
static bool drmvqueue_offer(DRMWQueue * queue, DelegateRequestEntry e);
static void drmvqueue_flush(DRMWQueue * queue);
static void drmvqueue_reset_fully_read(DRMWQueue *  queue);


static inline
int CAS_fetch_and_add(unsigned long * valueAddress, unsigned long incrementWith){
    int oldValCAS;
    int oldVal = ACCESS_ONCE(*valueAddress);
    while(true){
        oldValCAS = __sync_val_compare_and_swap(valueAddress, oldVal, oldVal + incrementWith);
        if(oldVal == oldValCAS){
            return oldVal;
        }else{
            oldVal = oldValCAS;
        }
    }
}

#ifdef CAS_FETCH_AND_ADD
#define FETCH_AND_ADD(valueAddress, incrementWith) CAS_fetch_and_add(valueAddress, incrementWith) 
#else
#define FETCH_AND_ADD(valueAddress, incrementWith) __sync_fetch_and_add(valueAddress, incrementWith) 
#endif 

static inline
unsigned long min(unsigned long i1, unsigned long i2){
    return i1 < i2 ? i1 : i2;
}

static inline
DRMWQueue * drmvqueue_create(){
    DRMWQueue * queue = (DRMWQueue *)malloc(sizeof(DRMWQueue));
    return drmvqueue_initialize(queue);
}

static inline
DRMWQueue * drmvqueue_initialize(DRMWQueue * queue){
    for(int i = 0; i < MWQ_CAPACITY; i++){
        queue->elements[i].request = NULL;
        queue->elements[i].data = 0;
        queue->elements[i].responseLocation = NULL;
    }
    queue->elementCount.value = MWQ_CAPACITY;
    queue->closed.value = true;
    __sync_synchronize();
    return queue;
}

void drmvqueue_free(DRMWQueue * queue){
    free(queue);
}

#define NEWOFFER
#ifdef NEWOFFER

static inline
bool drmvqueue_offer(DRMWQueue * queue, DelegateRequestEntry e){
    bool closed;
    load_acq(closed, queue->closed.value);
    if(!closed){
        int index = FETCH_AND_ADD(&queue->elementCount.value, 1);
        if(index < MWQ_CAPACITY){
            store_rel(queue->elements[index].responseLocation, e.responseLocation);
            store_rel(queue->elements[index].data, e.data);
            store_rel(queue->elements[index].request, e.request);
            __sync_synchronize();//Flush
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}

#else

static inline
bool drmvqueue_offer(DRMWQueue * queue, DelegateRequestEntry e){
    bool closed;
    load_acq(closed, queue->closed.value);
    if(!closed){
        int index = __sync_fetch_and_add(&queue->elementCount.value, 1);
        if(index < MWQ_CAPACITY){
            store_rel(queue->elements[index].responseLocation, e.responseLocation);
            store_rel(queue->elements[index].data, e.data);
            store_rel(queue->elements[index].request, e.request);
            __sync_synchronize();//Flush
            return true;
        }else{
            store_rel(queue->closed.value, true);
            __sync_synchronize();//Flush
            return false;
        }
    }else{
        return false;
    }
}

#endif


static inline
void drmvqueue_flush(DRMWQueue * queue){
    unsigned long numOfElementsToRead;
    unsigned long newNumOfElementsToRead;
    unsigned long currentElementIndex = 0;
    bool closed = false;
    load_acq(numOfElementsToRead, queue->elementCount.value);
    if(numOfElementsToRead >= MWQ_CAPACITY){
#ifdef NEWOFFER
        store_rel(queue->closed.value, true);
#endif
        closed = true;
        numOfElementsToRead = MWQ_CAPACITY;
    }

    while(true){
        if(currentElementIndex < numOfElementsToRead){
            //There is definitly an element that we should read
            DelegateRequestEntry e;
            load_acq(e.request, queue->elements[currentElementIndex].request);
            load_acq(e.data, queue->elements[currentElementIndex].data);
            load_acq(e.responseLocation, queue->elements[currentElementIndex].responseLocation);
            while(e.request == NULL) {
                __sync_synchronize();
                load_acq(e.request, queue->elements[currentElementIndex].request);
                load_acq(e.data, queue->elements[currentElementIndex].data);
                load_acq(e.responseLocation, queue->elements[currentElementIndex].responseLocation);
            }
            e.request(e.data, e.responseLocation);
            store_rel(queue->elements[currentElementIndex].request, NULL);
            currentElementIndex = currentElementIndex + 1;
        }else if (closed){
#ifdef QUEUE_STATS
            helpSeasonsPerformed.value++;
            numberOfDeques.value = numberOfDeques.value + currentElementIndex;
#endif
            //The queue is closed and there is no more elements that need to be read:
            return;
        }else{
            //Seems like there are no elements that should be read and the queue is
            //not closed. Check again if there are still no more elements that should
            //be read before closing the queue
#ifdef WAITS_BEFORE_CLOSE_QUEUE_ATTEMPT
            for(int i = 0; i < WAITS_BEFORE_CLOSE_QUEUE_ATTEMPT; i++){
                __sync_synchronize();                
            }
#endif
            load_acq(newNumOfElementsToRead, queue->elementCount.value);
            if(newNumOfElementsToRead == numOfElementsToRead){
                //numOfElementsToRead has not changed. Close the queue.
                numOfElementsToRead = 
                    min(get_and_set_ulong(&queue->elementCount.value, MWQ_CAPACITY + 1), 
                        MWQ_CAPACITY);
#ifdef NEWOFFER
                store_rel(queue->closed.value, true);
#endif
		closed = true;
            }else if(newNumOfElementsToRead < MWQ_CAPACITY){
                numOfElementsToRead = newNumOfElementsToRead;
            }else{
#ifdef NEWOFFER
                store_rel(queue->closed.value, true);
#endif
                closed = true;
                numOfElementsToRead = MWQ_CAPACITY;
            }
        }
    }
}

static inline
void drmvqueue_reset_fully_read(DRMWQueue * queue){
    store_rel(queue->elementCount.value, 0);
    store_rel(queue->closed.value, false);
}



//QD Lock


typedef struct AgnosticDXLockImpl {
    DRMWQueue writeQueue;
    char pad1[128];
    void (*defaultWriter)(int, int *);
    char pad2[64 - sizeof(void * (*)(void*)) % 64];
    char pad3[128];
    TATASLock lock;
    char pad4[64];
} AgnosticDXLock;


AgnosticDXLock * adxlock_create(void (*writer)(int, int *));

void adxlock_initialize(AgnosticDXLock * lock, void (*defaultWriter)(int, int *));

static inline
void adxlock_free(AgnosticDXLock * lock){
    free(lock);
}

static inline
void adxlock_register_this_thread(){
}


void adxlock_write_with_response(AgnosticDXLock *lock, 
                                 void (*delgateFun)(int, int *), 
                                 int data, 
                                 int * responseLocation);

int adxlock_write_with_response_block(AgnosticDXLock *lock, 
                                      void (*delgateFun)(int, int *), 
                                      int data);
void adxlock_delegate(AgnosticDXLock *lock, 
                      void (*delgateFun)(int, int *), 
                      int data);

void adxlock_write(AgnosticDXLock *lock, int writeInfo);

static inline
void adxlock_write_read_lock(AgnosticDXLock *lock) {
    tataslock_write_read_lock(&lock->lock);    
    drmvqueue_reset_fully_read(&lock->writeQueue);
    __sync_synchronize();//Flush
}

void adxlock_write_read_unlock(AgnosticDXLock * lock);

static inline
void adxlock_read_lock(AgnosticDXLock *lock) {
    adxlock_write_read_lock(lock);
}

static inline
void adxlock_read_unlock(AgnosticDXLock *lock) {
    adxlock_write_read_unlock(lock);
}



#endif
