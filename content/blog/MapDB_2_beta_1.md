+++
title = "MapDB 2 beta 1 is out"
template = "page.html"
description = "Beta 1 is out. It brings storage format and API freeze into MapDB 2.0 branch. This format and API should be supported for several years to come. Stable MapDB 2.0 will share the same format. Also latter 2.1 release with performance optimizations and long-term support will use the same."
path = "blog/MapDB_2_beta_1"
date = 2015-06-29
[extra]
render_title = false
+++

MapDB 2 beta 1 is out
=======================

Beta 1 is out. It brings storage format and API freeze into MapDB 2.0 branch.
This format and API should be supported for several years to come.
Stable MapDB 2.0 will share the same format. Also latter 2.1 release with performance 
optimizations and long-term support will use the same.

<!-- more -->
 
Bug wise beta 1 should be "stable enough" for yearly adopters. 
It has most bugs fixed, and newly discovered issues are fixed fast. 
If you have new project or you are investigating MapDB, 
I would recommend you to give it a try over old 1.0 version.

There is also work-in-progress 
[new manual](http://www.mapdb.org/doc/index.html) for 2.0 branch. Also 
[PDF version](http://www.mapdb.org/_downloads/mapdb-manual.pdf) is available. 

Bugs
------
MapDB 2.0 beta 1 passed some smoke tests and it seems to be stable.
However some areas need more tests:

List of possible problems includes:

 * Crash recovery for Write-Ahead-Log and compaction is not completely verified. 
  Data should be safe, but recovery might require user intervention to delete some old files etc.
     
 * MMap files could [cause JVM to crash](https://github.com/jankotek/mapdb/issues/442). 
    Older 1.0 branch also has this bug, it should be fixed in two weeks in 1.0.8 and 2.0-beta2.

 * AppendOnly store does not have compaction. It also needs more testing for crash recovery.          

 * Several performance optimizations are disabled. Stability over speed is preferred. Many parts could be 4x faster,
 but those optimizations are postponed to 2.1 release. However 2.0 is still much faster compared to 1.0 release.
  
I would recommend current release for in-memory caching or computation.
And I would be careful with reliable on-disk storage.
  
Changes from 1.0
--------------------
MapDB 2.0 should be compatible with 1.0 at API level (``DBMaker`` and ``DB`` classes). 
However old methods are deprecated and will be removed in 2.1. 
There are [several new features](/blog/MapDB_20_is_near/), but lets talk about 
possible migration issues:

 * All methods from 1.0 are present. If you get compilation error please open bug.

 * There is no migration tool yet for 1.0 users. I am working on export/import tool which will dump database content
  into JSON. 
  
 * MapDB storage now uses single file instead of two. Some temporary for WAL and compaction might be created.    
 
 * `DB.getSomething()` methods were renamed to `DB.something()` (no get). It is better for code assistant. 
    Old methods are still present, but are deprecated.
    
 *  `DB.createSomething()` methods were renamed to `DB.somethingCreate()` (no get). It is better for code assistant. 
        Old methods are still present, but are deprecated.  
  
 * Queues are now deprecated and will be removed (replaced) in 2.1 release. 
 I am not happy with current implementation and will make new one with more options and features.
  
 * Instance cache is disabled by default in 2.0. It could mean bad performance in many applications. 
  Use `DBMaker.cacheHashTableEnable()` to reenable them`
  
 * Tuples are gone, too many classes to maintain. There is `Fun.Pair` for two keys. But I would recommend
  Object[] arrays for composite `BTreeMap` keys.  There is ``BTreeKeySerializer.ArrayKeySerializer`.
  
 * Default file access method changed from `FileChannel` to `RandomAccessFile`. That 
  could mean worse performance for non-mmap files. Use `DBMaker.fileChannel()` to enable old method.
 
 * MapDB 2.0 still works with Java 6. But we might migrate to 
    [Java 7 and Kitkat](https://groups.google.com/forum/#!topic/mapdb/DAl_jY3HMn4). 
    Speak now if you need Java 6.
    
 * MapDB now contains reference to `sun.misc.Unsafe`. To compile for Android, delete `UnsafeStuff.java` and related tests. 
    It will still run. Better Android support will be provided with code preprocessor latter.

Next turn
-------------

Right now MapDB is about bug-fixing. I started resolving 100+ open issues on github. MapDB 1.0.8 and Beta 2 
will come in one maybe two weeks. It should solve most pressing issues with reliability. 
Also migration/backup tool is important.

There will be more incremental development from now on. New beta release should be out every two weeks. Stable 2.0 
is expected in September or October. 

MapDB is turning from technical problem to social problem. 
I changed my daily schedule. Now I will answer questions in a two or three days (instead of weeks).
Do not worry to [drop me a line directly](mailto:jan.at.kotek.net), 
mailing list and issue tracker are not strictly required.
I will also blog more often and restart my Youtube channel. 

I would be happy to do quick free consulting over phone,  in exchange for your testimonial on *mapdb.org* website.
Some pretty big companies are using MapDB (and JDBM) for years, but we can not name them for various reasons.
 
We also provide paid consulting for MapDB. Usually the problems are not strictly MapDB specific, 
but are also related to data-modeling. This sort of general questions are not answered on public mailing list.
And finally once stable 2.0 is out we will provide commercial support subscription.

Personally I am very satisfied. Beta 1 release is a huge personal milestone for me. 
And something happy recently happened in my family life. It solved problem we were having for past a few years, 
and already improved my development productivity a lot.
