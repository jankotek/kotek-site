+++
title = "JDBM 2.1 and beyond"
template = "page.html"
description = "JDBM 2.0 was released just a few weeks ago, now is time to start working on new version. JDBM 2.1 will bring fixes and performance improvements, but keeping file format and API compatible with 2.0."
path = "blog/jdbm_2.1_and_beyond"
date = 2011-01-16
[extra]
render_title = false
+++

JDBM 2.1 and beyond
======
JDBM 2.0 was released just a few weeks ago, now is time to start working on new version. JDBM 2.1 will bring fixes and performance improvements, but keeping file format and API compatible with 2.0.

<!-- more --> 


Small changes
----
Important change is to improve concurrency of soft cache. This should solve 60% concurrency performance problems. Now JDBM uses single lock for cache and storage, this means cache is blocked when storage reads from disk. Finer grade locks would reduce unnecessary cache locking. Same apply to BTrees.  There is already [patch for this](http://code.google.com/p/jdbm2/issues/detail?id=1).

JDBM 2.0 currently does not have fail fast iterators on maps. So if you insert new record while iterating, opened iterator returns an unexpected result. An [ConcurrentModificationException](http://download.oracle.com/javase/6/docs/api/java/util/ConcurrentModificationException.html) should be thrown instead.

Opening store by multiple JDBM instances should fail. Current file lock is based on FileChannel, but it does not seems to be reliable on all OS. JDBM 2.1 will have new file locking mechanism similar to H2Database. 

Other small improvement are custom serializers for HTree and a few accessors. Checkout [those patches](https://github.com/fusesource/jdbm/commits/fusesource-2.0.x).

Maven2 seems to be very popular for JDBM developers. In fact this project has migrated from Ant to Maven2 independently about 3x times. I personally prefer Ant, but will not hold back. JDBM 2.1 will remove Ant and use Maven2. There should also be an 'official' JDBM 2.1 release in Maven2 repositories. 

There is question if JDBM should move to Github. I am very happy Githubber and have tons of stuff in there. But on other side, Google Code gives me better control over source code and storage file format (this was big problem in JDBM 1.x). For now I will leave this question open.

And wow, JDBM has actual users and [bug reports](http://code.google.com/p/jdbm2/issues/list)!! Of course, all bugs are going to be fixed. 

BTree & Htree fragmentation
---
Most pressing performance problem is index fragmentation. When new record is inserted, JDBM will simply use nearest free record.If an index is frequently updated, it may lead to very poor performance as index get more fragmented. JDBM 2.0 has defrag() method. But this only rearranges record by insertion time, and frees unused space. It does not make 'real' defragmentation by reordering tree nodes. 

For JDBM 2.1 I plan two improvements which should solve 90% of this issue. First new records should be inserted into 'groups', this would significantly reduce fragmentation on bulk updates. 

Second improvement is to fix defrag() method to really sort tree records. But to fully fix this issue, I would have to change file format. So improved defrag() will work only in a few custom cases (keys and values are numbers or strings). 

JDBM 3.0
---
I already have plans for new major version, which would require new file format. 

Current btree and htree format prevents full tree defragmentation. JDBM can not read all nodes in tree without deserializing all it's values and keys. This is related to custom serializers and variable record size. JDBM 2.1 have partial workaround. But full fix requires change in file format.

JDBM 1.0 and 2.0 stores values as part of tree nodes. This is very fast for small values and keys, but does not work well with large values. JDBM 2.0 introduced 'PrimaryStoreMap' as workaround. In JDBM 3.0 only small values will be stored as part of tree nodes. If serialized value would exceed 64 bytes, new record will be created, and tree node will store only reference. This reference will be lazily loaded and auto deleted/updated. 

Other major change would be serialization. JDBM 2.0 uses custom space efficient serialization for a few base classes (Long, Integer, ArrayList...). I have plan to dump Java serialization for all classes. Serialization usually contains two data: class description and serialized data. Java serialization stores 'class description' on each record and thus creates big space overhead. Goal of new serialization is to store 'class description' only once. BerkleyDB has similar feature and it works very well for them. 


JDBM 4.0
---
I am big fan of Scala and concurrency. So new major version may be written from scratch in Scala with Actors or STM. Also I am fascinated with [Kilim lightweight threads](http://kilim.malhar.net/)

Other option is to merge JDBM2 with H2 database. We have a lot of unique features (btree delta compression, efficient serialization...) and H2 could really benefit. On other hand JDBM would finally get full Concurrent Transaction Isolation and very fast engine from H2.
