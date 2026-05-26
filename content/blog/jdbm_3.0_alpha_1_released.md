+++
title = "JDBM 3.0 alpha 1 released"
template = "page.html"
description = "I am proud to announce first alpha of JDBM3. JDBM is embedded Java key value database with more than 10 years of history. It provides java collections (maps, sets and lists) backed up by disk storage. And it has unbeatable performance and simplicity."
path = "blog/jdbm_3.0_alpha_1_released"
date = 2012-01-18
[extra]
render_title = false
+++

JDBM 3.0 alpha 1 released
====

I am proud to announce first alpha of JDBM3.  JDBM is embedded Java key value database with more than 10 years of history. It provides java collections (maps, sets and lists) backed up by disk storage. And it has unbeatable performance and simplicity.

<!-- more -->

Main change from JDBM2 is write performance. JDBM is now probably the fastest Java db ever. It inserts million records per second. It creates multi-terabyte store with 1e11 records overnight. Instance cache now scales up-to 64 GB RAM. And it uses mapped memory buffers to maximize disk IO speed. 

JDBM3 also introduces new deadly simple API. Everything from JDBM1 is gone (package protected). JDBM3 exports only two public classes. New release brings much more features, but is also simpler to use. 

List of main new features
=====

Compact serialization
----
JDBM has serialization with very little overhead. Compared to java serialization it uses 100x less space. It also stores class definition outside of records on single space. Serialization in this alpha seems to be working fine, but some corner cases (Externalizable, inner classes) are not handled correctly. 

Write performance improvements
----
I spend huge amount of time making sure JDBM is fast with disabled transactions. Most of slow hot spots were identified and optimized away. Mapped byte buffers are now used, so random inserts have minimal penalty. JDBM can now truly insert million records per second (at least on my 5GHz computer with SSD drive). But JDBM makes 200 000 records/s even on an old laptop with slow disk.

API simplification
----
API was greatly simplified. 'RecordManager' was renamed to 'DB'. There is new builder for configuration, no more verbose properties. BTree/HTree and direct recid access are now obsolete(and gone) by collections. JDBM was merged into single package and most of internal stuff is package protected. I may have went too far, so I am open to discussion about making some old APIs public again.

Cache improvements
----
There are two new cache types using hard and weak references. 'Hard' cache has very little overhead (does not have to maintain reference queue) and scales well up to 64GB Heap. JDBM now periodically checks free mem and if its less than 25%, it clears reference cache. It is necessary for hard cache and I found GC to be slow and unreliable with huge heap. MRU cache is now default safe option.

Mapped memory disk buffer
----
JDBM now uses mapped memory disk buffer. This is very fast and advance way to access disk. JDBM3 now has nearly zero data copying and unbeatable performance. Mapped buffer is on by default, but there is an option to fallback into RandomAccessFile. 

New collections
----
JDBM3 adds TreeSet and HashSet which are basically maps without values. It also adds LinkedList which is completely new structure. Secondary maps, StorageSet and some other stuff from JDBM2 is gone, but I am open to discussion about implementing it again.

New storages
----
If you specify 'null' instead of filename, JDBM will store all data in-memory. So data access is very fast, but data will be lost after JVM restarts. Other storage options are in progress and do not work well in this alpha (encryption, zip, write overlay). 

Maven2
----
JDBM is now fully mavenized. I will add it to public reps when it reaches beta.

Defragmentation
----
Defrag is now much better. It reorders records so collections are stored at the same pages. This makes trees much faster.

Large values stored outside of tree
----
Large values are no longer inlined in trees. If it is bigger than 32 bytes, it is stored as separate record and load lazily.

Readonly store
----
Now it is possible to open store in readonly mode. This uses different locking, so you can open one file using more JVM instances in readonly mode. It also means that data are read faster as JDBM does not have to create defensive copies. 

Usage
----
JDBM is located at [github repository](https://github.com/jankotek/JDBM3). You can download compiled jar file [here](https://github.com/downloads/jankotek/JDBM3/JDBM-3.0-alpha-1.jar). There is no javadoc yet, just follow those two [simple](https://github.com/jankotek/JDBM3/blob/master/src/main/java/net/kotek/jdbm/DBMaker.java)  [class](https://github.com/jankotek/JDBM3/blob/master/src/main/java/net/kotek/jdbm/DB.java) or example on main page.  

This release is usable, but contains bugs and many TODOs!  Its main purpose is to get feedback from  community. 

Future and other stuff
----
I got married and reevaluated my opensource activities.  JDBM is very compact, with good code quality, successful  and with huge potential. Exactly as a personal hobby project should be. So I suspended my other projects and work now solely on JDBM. 

As you may have noticed I renamed 'jdbm' package to 'net.kotek.jdbm'. I founded previous package name too generic. New package should reduce fragmentation (there already 10  JDBM forks). It should be clearly visible where 'official' page is. 

I expect JDBM3 to reach beta stage in about 6 months. At this point JDBM will turn into regular project with documentation, bug tracking system, maven2 repo etc.. There will also be feature freeze.

I believe JDBM3 has potential to be used by millions of people. So final version should be much better tested than JDBM2. I have automatic test suite, which hammers JDBM with random data for several weeks (or months). But before final JDBM release I will try to get sponsors, some extra hardware and adds could really speedup release. 

At current speed I expect to have final JDBM 3 in two years.
