+++
title = "Announcing JDBM4"
template = "page.html"
description = "The JDBM3 project has been quiet for the last few weeks, but a lot has happened in between. I talked about JDBM3 at the Geecon conference in front of 50 people. I also met a handful of JDBM users. Results were not very encouraging. JDBM3 is very fast, but it is synchronized on single-big lock and does not scale well with concurrent access on multi core CPUs. And for most people this can be a deal breaker."
path = "blog/announcing_JDBM4"
date = 2012-06-08
[extra]
render_title = false
+++

Announcing JDBM4
================

The JDBM3 project has been quiet for the last few weeks, but a lot has happened in between. I talked about JDBM3 at the Geecon conference in front of 50 people. I also met a handful of JDBM users. Results were not very encouraging. JDBM3 is very fast, but it is synchronized on single-big lock and does not scale well with concurrent access on multi core CPUs. And for most people this can be a deal breaker.

<!-- more --> 

Another basic problem with JDBM3 is its writing performance in transactional mode. It can be a bit unpredictable and usually is 10x slower than non-transactional write. This is a result of fixed size page store, so inserting a 100 byte record can result in 16KB being transferred.

JDBM code was under linear development for 12 years. I developed JDBM2 and JDBM3 in the form of incremental-test-driven changes into the original JDBM 1 code. During the last 4 years I introduced new features (Maps, caches, serialization..) into already existing code. Some changes were radical, but it was always possible to re-factor existing code to support them.

But introducing concurrency and new transaction log into the existing code would be a dead-end. So I decided to drop the development of JDBM3 and start writing JDBM4 from scratch. From now on JDBM3 is in maintenance mode and I will only fix critical bugs (data corruption). I am probably breaking a few promises here, but JDBM3 never reached 'beta' stage.

So lets talk about JDBM4. I spent the last few weeks designing and developing it. The JDBM4 design is nearly completed and about 20% of the code is already written. I will put the first version on Github in about 8 weeks. In order to implement concurrency well I had to radically simplify JDBM internals. Compared to JDBM3 the  new code  is more compact, consistent and readable.

So here are some changes:

Fine grained locking
--------------------
All layers in JDBM4 will take advantage of fine grained locking. So JDBM4 performance should scale nearly linearly with a number of cores. This brings some challenges, such as non-thread-safe NIO buffers, but I probably have enough experience to work around those. JDBM4 will mostly use `ReentrantReadWriteLock` so the read-only mode should be completely lock free. For write locking we can take advantage of instance cache and do all the locks in memory and lazily. Also there are many tricks available, such as back-ground write thread.

BTree and HTree locking brings other challenges. My plan is to implement per tree node locks. There is instance cache so node locks can be implemented in memory. 

I also plan to introduce new lock-free index tree, probably Skip List.

Locks can be disabled
---------------------
Many users are using JDBM in a single thread environment, and they should not pay the price for fine grained locking. So there will be a switch to disable all locks. In this mode JDBM will run slightly faster, but will be thread unsafe. It will also enable some features which will be unavailable in concurrent mode (such as MRU cache). 

Page store layer eliminated 
---------------------------
The previous version had a fixed size page store. Variable size records were implemented on top of this layer as linked lists. This layer was also responsible for transactions, dirty records and so on. But this layer is not necessary in this version so it has been eliminated. 

Instruction based transaction log
---------------------------------
JDBM3 has fixed size page based transaction log. Modifying single byte in transaction mode would make a 4KB page dirty, and the entire page would be written into transaction log. Inserting single 100B record could actually result in 16 KB IO operations. In JDBM4 the transaction log will be 'instruction based'. The previous version effectively had single instruction 'write 4KB at this offset'. JDBM4 adds instructions such as 'write this long value at this offset'. This reduces the number of IO operations in transactional mode by several magnitudes. 

Simplified store 
-----------------
There are many simplifications in RecordStore (aka RecordManager). For example the maximal record size will be 64KB, larger records will be transparently stored in separate files. Records will also no longer be stored as linked list. The record size will be stored in the index file together with its physical offset. This simplifications should reduce the number of IO operations, make performance more predictable and concurrency easier. 


RecordStore decorators
----------------------
JDBM3 implemented instance cache as `decorator` for originally non-cached RecordStore. JDBM4 will take this approach even further. It will be possible to chain `RecordStore` decorator to get the functionality you need. For example there should be decorator for MVCC, background write thread, write union, write logs and so on. Chaining should keep internal architecture simple and more modular


Lock free instance cache
------------------------
Current instance cache is implemented as `HashMap<Long,Object>`. When new object is fetched from store, entire cache is completely locked while adding new record into cache. There are better options such as lock free `SkipListMap`.
