+++
title = "JDBM4 now open for public"
template = "page.html"
description = "After 4 months of development JDBM4 is now stable enough for the first public testing. Now is good time for any early adopters or possible contributors to take JDBM4 for a quick spin."
path = "blog/JDBM4_now_open_for_public"
date = 2012-09-16
[extra]
render_title = false
+++

JDBM4 now open for public
=========================

After 4 months of development [JDBM4](https://github.com/jankotek/JDBM4) is now stable enough for the first public testing. 
Now is good time for any early adopters or possible contributors to take JDBM4 for a quick spin.

<!-- more --> 

JDBM4 is a complete rewrite of the JDBM 1/2/3 code base. The goal for this generation was to achieve
concurrent scalability and faster transactions. The 12 years old codebase in JDBM3 could not 
support such massive changes and complete rewrite was necessary. Dropping the existing-stable code is always 
risky, but it worked very well for JDBM4. The new JDBM code is more compact, 
readable and maintainable. The performance also seems to be superior to JDBM3. 
 

RecordStore
-----------
The RecordStore was dramatically simplified. Fixed-size-page layer was removed, now variable-size records
are stored directly on disk. A new data structure `LongStack` was introduced to support free logical 
and physical records lists. LongStack saves a lot of code duplication. 
The new RecordStore is now in a single class (compared to dozen in JDBM3). 

There is also a new storage format. It reduces the per-record overhead to 8 bytes (used to be 9 bytes in JDBM3). This way all record information fits into a 64-bit-long, which greatly simplifies the store. 
It uses 16 bites as the record size and 48 bites as the storage offset. The maximal store size is currently 281 terabytes. 

The RecordStore currently does not support records bigger than 64KB. This will be fixed.


Asynchronous writes
------------------------
The RecordStore needs atomic updates, this would be comprex with fine grained locking. The solution is to queue all writes into separate background thread. As a result, JDBM4 now has faster insert/update/remove operations even in 
single-threaded mode. 


Modular RecordManager
------------------------
JDBM3 was tightly integrated together and had a very minimalistic public API (DB, DBMaker). 
I believed this was for maximal performance, but in reality it was just an excuse 
not to expose legacy code. JDBM4 now has a clean separation to modules while keeping up with the
performance. 

The center piece of this modularity is the `RecordManager` interface. For example, instance 
cache is implemented as RecordManager wrapper. JDBM4 can use alternative 
record store, so that other databases, such as LevelDB, Kyoto etc can now 
take advantage of JDBM4 maps, instance cache and advanced serialization.

This modularity also opens interesting networking possibilities. 
With `RecordManager` wrapper JDBM4 can communicate over a network socket. 
I can imagine some sort of write-master-readonly-slaves cluster similar to
MySQL; or central store and fat clients, each with its own instance cache...


Concurrent B-Linked-Tree
------------------------
BTree is the mostly used index in JDBM. BTrees are usually not concurrent, so I needed a similar 
concurrent-safe structure which would not require global lock. The solution to that
is [B-Linked-Tree](http://www.cs.cornell.edu/courses/cs4411/2009sp/blink.pdf). 

It has a similar structure as BTree, but each node stores additional link to the next node at the same level.
Node split is performed in a special sequence, so that the tree structure is never broken. 
Inserts/updates typically require only single node to be locked at a time. 
Reads are never blocked. 
This tree requires memory operations to be atomic; not so good for RAM, but perfect 
for database. It is simply great concurrent BTree for JDBM4. 

A theoretical paper is always hard to implement. Luckily 
[Thomas Dinsdale-Young](https://www.doc.ic.ac.uk/~td202/) wrote 
[practical  demonstration](https://www.doc.ic.ac.uk/~td202/btree/) of this algorithm. 
This saved us a great amount of time and BTreeMap is directly based on this demo. 

Trade-off are deletes which cause tree fragmentation. So after a massive delete we 
may have to run tree defragmentation. I will implement some workarounds.
Another trade-off is bidirectional navigation. It is required for `NavigableMap`, but
concurrent algorithm does not support it. So I replaced `ConcurrentNavigableMap` 
with JDBM4 specific `ConcurrentSortedMap` interface. This also removes dependecy on Java6 API, so JDBM4 can run on Android prior 2.3 version. 

Implementation in JDBM4 is only half finished. It supports all methods on Map and ConcurrentMap interfaces.
SortedMap methods are not implemented yet. It also needs concurrency tests. And delta compression 
on keys is also missing. 

TreeMap in JDBM4 should be usable and  as fast as in JDBM3. 
Insert/Update performance should also scale linearly with the number of cores. 

Concurrent HTreeMap
-------------------
To support concurrent scalability, it was split into 16 segments, each with separate `ReentrantReadWriteLock`.  `ConcurrentHashMap` works in a similar way. This is a very simple and effective way to support concurrency. 

I was not sure if HTree should be part of JDBM4, as having two very similar trees would be duplication. 
So HTree in JDBM4 was optimized for large key/values. Those are no longer stored in tree nodes, 
but in a separate record. That is for the best performance use of BTree with small keys and HTree with large keys. 

HTree in JDBM4 should scale well up to 1e9 records; this limit is due to the 32bit java hash. 

HashMap in JDBM4 should be fully finished. I dont expect any changes other then bugfixes. 

Not yet implemented stuff
-------------------------
 * Transactions (I need one rainy weekend to implement this)
 * Weak/Soft/MRU cache (only hard ref cache is currently implemented)
 * POJO serialization (only basic serializer for java.util and java.lang classes)
 * Custom serializers on Maps
 * Max record size is currently 64KB.
 * Defrag

Contributing
------------
JDBM4 is now perfectly ready for contributors. The existing code is clean, well documented and unit-tested. 
JDBM4 will probably trigger a small revolution in Java persistence and contributing is a great way 
to get recognized. 

If you find some of this stuff interesting, drop me a line on [github](https://github.com/jankotek/JDBM4) or 
directly by email at: jan at kotek dot net.

You may hava a look at: 

**POJO serialization** was working in JDBM3. But it uses Sun/Oracle API and does not run on Android. 
Also it is a bit messy and could use rewrite. I would be very happy to completely handover this part
to somebody else. But I would also prefer if it would stay as part of the JDBM4 package. 

**Performance tests.** JDBM4 has great performance. It needs performance tests 
which would compare its performance to other similar DBs (LevelDB, Kyoto, H2, JDBM3). 
It should also test concurrent scalability. And periodic performance tests are 
also important to discover performance regression bugs. 
Maintaining such test suite is not a trivial task, and I would appreciated if someone would take it over.

**Soft/Weak/MRU cache.** Instance caches in JDBM3 were fast but a messy code. Currently we only have
hard reference cache (`RecordHardCache`). Thanks to modular `RecordManager` it is easy to 
implement new caches. But this task requires a lot of performance testing, fiddling and polishing. 


**Concurrent unit tests.** JDBM4 should have great concurrent scalability, but right now there are very few concurrent tests (I only proved it, not tested :-)). So we need tests which would "hammer" the db with random stuff in multiple threads. 

**Deque collection.** JDBM4 needs LinkedList implementation. Since LinkedList does not support sequential access, it should only implement double-ended-queue (Deque interface). Optionally it should implement BlockingDeque.

**Daily builds** it would be great to have Hudson with daily builds and Maven repository. 

**Testing hardware** I would love to test JDBM4 on some decent iron. My current machine (Quad CPU at 5GHz, 16GB RAM, 1 TB storage) is insufficient. Could someone borrow me a machine with 16 CPUs, 128 GB RAM or 10 TB storage for a couple of weeks?. Also some decent SSD would be welcomed.


What is next
------------
JDBM4 will enter alpha after transactions, POJO serialization and a few tweaks are finished. This will happen in
about a month. Alpha versions will be available in central maven repository.
