#ifndef KVSET_HPP
#define KVSET_HPP KVSET_HPP

#include <cstdlib>
#include "kvset.h"

/**
 * @internal
 * @brief stub comparison function
 * @param K key type
 * @param A ignored
 * @param a first key
 * @param b second key
 * @warning as keys are supposed to be pointers this will always return garbage
 */
template<typename K, typename  A>
int default_compare(K a, K b, A) { return a - b; }


/**
 * @internal
 * @brief coding shorthand for compare, allocation and freeing functions
 * @param KeyType type of key for comparison
 * @param Additional type of additional parameter to comparision function
 * @param Compare comparison function
 * @param Malloc memory allocation function
 * @param Free memory freeing function
 */
template <
	typename KeyType,
	typename Additional = void*,
	int (*Compare)(KeyType, KeyType, Additional) = default_compare<KeyType, Additional>,
	void* (*Malloc)(size_t) = std::malloc,
	void (*Free)(void*) = std::free
>
struct standard_functions {
	/** @brief comparision function wrapper */
	static int compare(KeyType a, KeyType b, Additional add) { return Compare(a, b, add); }
	
	/** @brief freeing function wrapper */
	static void free(void* data) { Free(data); }

	/** @brief memory allocation function wrapper */
	static void* alloc(size_t size) { return Malloc(size); }
};

/**
 * @internal
 * @brief typesafe wrapper if kv_set
 * @param T real type of the type specific data (void* in C version)
 * @see kv_set
 */
template<class T>
struct kv_set_t {
	KVSetFunctions funs;
	unsigned int key_offset;
	T type_specific_data;
};

/**
 * @internal
 * @brief wrapper to C interface
 * @param Instance a kv_set_instance, target of delegation
 * 
 * This class specifies functions in accordance with what the C interface expects,
 * but delegates all calls to the member functions of kv_set_instance.
 * This is required so that normal C++ coding can be used transparently to the C interface.
 */
template <typename Instance>
class kv_set_classfuns {
	typedef typename Instance::key_type KeyType;
	typedef typename Instance::value_type Obj;
	public:
		static void* put(kv_set* s, void* key) {
			auto result = reinterpret_cast<kv_set_t<Obj>*>(s)->
				type_specific_data.
				put(
					static_cast<KeyType>(key)
				);
			return static_cast<void*>(result);
		}
		static int put_new(kv_set* s, void* key) {
			auto result = reinterpret_cast<kv_set_t<Obj>*>(s)->
				type_specific_data.
				put_new(
					static_cast<KeyType>(key)
				);
			return result;
		}
		static void* remove(kv_set* s, void* key) {
			return static_cast<void*>(reinterpret_cast<kv_set_t<Obj>*>(s)->type_specific_data.remove(static_cast<KeyType>(key)));
		}
		static void* lookup(kv_set* s, void* key) {
			return static_cast<void*>(reinterpret_cast<kv_set_t<Obj>*>(s)->type_specific_data.lookup(static_cast<KeyType>(key)));
		}
		static int member(kv_set* s, void* key) {
			return reinterpret_cast<kv_set_t<Obj>*>(s)->type_specific_data.member(static_cast<KeyType>(key));
		}
		static void* first(kv_set* s) {
			return static_cast<void*>(reinterpret_cast<kv_set_t<Obj>*>(s)->type_specific_data.first());
		}
		static void* last(kv_set* s) {
			return static_cast<void*>(reinterpret_cast<kv_set_t<Obj>*>(s)->type_specific_data.last());
		}
		static void* next(kv_set* s, void* key) {
			return static_cast<void*>(reinterpret_cast<kv_set_t<Obj>*>(s)->type_specific_data.next(static_cast<KeyType>(key)));
		}
		static void* previous(kv_set* s, void* key) {
			return static_cast<void*>(reinterpret_cast<kv_set_t<Obj>*>(s)->type_specific_data.previous(static_cast<KeyType>(key)));
		}
};


/**
 * @internal
 * @brief convenience wrapper to datastructure implementations
 * @param DataType the mapping datastructure in use
 * @param KeyType key for the DataType
 * @param StdFuns comparison, allocation, and freeing functions
 *
 * This wrapper simply adds a few convenience typedefs to the DataType implementation.
 */
template <template<typename, class> class DataType, typename KeyType, class StdFuns = standard_functions<KeyType>>
class kv_set_instance {
	typedef DataType<KeyType, StdFuns> Impl;
	public:
		kv_set_instance() : inst() {}
		KeyType put(KeyType key)     { return inst.put(key); }
		bool put_new(KeyType key)    { return inst.put_new(key); }
		KeyType remove(KeyType key)  { return inst.remove(key); }
		KeyType lookup(KeyType key)  { return inst.lookup(key); }
		bool member(KeyType key)     { return inst.member(key); }
		KeyType first()              { return inst.first(); }
		KeyType last()               { return inst.last(); }
		KeyType next(KeyType key)    { return inst.next(key); }
		KeyType previous(KeyType key){ return inst.previous(key); }
		
		typedef kv_set_classfuns<kv_set_instance<DataType, KeyType, StdFuns>> classfuns;
		typedef StdFuns stdfuns;
		typedef KeyType key_type;
		typedef Impl value_type;
	private:
		Impl inst;
};

/**
 * @internal
 * @brief generic cleanup code
 * @param set the table to delete
 * @param f ignored (for now)
 * @param context ignored 
 * @todo delete elements in the table before deleting table
 *
 * Deletes a mapping datastructure and frees any allocated memory.
 * This cannot be a member function of the structure to be freed,
 * so it is implemented as a separate template function.
 */
template <template<typename, class> class Impl, typename K, class S>
void delete_table(kv_set* set, void (*f)(void* context, void* element), void* context) {
	typedef kv_set_instance<Impl, K, S> FS;
	//TODO delete elements in table here
	reinterpret_cast<kv_set_t<FS>*>(set)->type_specific_data.~FS();
	FS::stdfuns::free(s);
}


/**
 * @brief create a kv_set (usable in C) from a C++ datastructure
 * @param Impl the C++ datastructure
 * @param K the mapping key
 * @param S comparison, memory allocation and freeing functions
 * @return a kv_set wrapping the specified C++ datastructure
 *
 * Use this in the form
 * auto kvs = make_kv_set<MyDataStructure>();
 * to create a kv_set of MyDataStructure.
 * Remember that you have to collect the allocated memory using
 * destroy_kv_set(kvs);
 */
template <template<typename, class> class Impl, typename K = long*, class S = standard_functions<K>>
kv_set* make_kv_set() {
	typedef kv_set_instance<Impl, K, S> FS;
	void* memory = FS::stdfuns::alloc(sizeof(KVSet) + sizeof(FS));
	kv_set* r = static_cast<kv_set*>(memory);
	new (&r->type_specific_data) FS;
	r->funs.delete_table = &delete_table<Impl, K, S>;
	r->funs.put = &FS::classfuns::put;
	r->funs.put_new = &FS::classfuns::put_new;
	r->funs.remove = &FS::classfuns::remove;
	r->funs.lookup = &FS::classfuns::lookup;
	r->funs.member = &FS::classfuns::member;
	r->funs.first = &FS::classfuns::first;
	r->funs.last = &FS::classfuns::last;
	r->funs.next = &FS::classfuns::next;
	r->funs.previous = &FS::classfuns::previous;
	
	return r;
}

/**
 * @brief deallocate a kv_set constructed around a C++ datastructure
 * @param s the kv_set to destroy
 */
void destroy_kv_set(kv_set* s) {
	s->funs.delete_table(s, nullptr, nullptr);
}

#endif
