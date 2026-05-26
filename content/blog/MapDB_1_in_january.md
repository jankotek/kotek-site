+++
title = "MapDB 1.0 will be released in January"
template = "page.html"
description = "If you follow me on Github, you may have noticed I started preparations for 1.0 release. Some features were moved after 1.0, a long manual is slowly growing and number of remaining TODOs is shrinking fast."
path = "blog/MapDB_1_in_january"
date = 2013-11-06
[extra]
render_title = false
+++

MapDB 1.0 will be released in January
======================================

If you follow me on Github, you may have noticed I started preparations for 1.0 release. 
Some features were moved [after 1.0](https://github.com/jankotek/mapdb/issues?labels=after+1.0), 
a long manual is [slowly growing](https://github.com/jankotek/MapDB/tree/master/src/site/markdown/doc) and 
number of remaining TODOs is shrinking fast.

<!-- more --> 

So I am happy to announce that everything is on track for MapDB 1.0 to be released on January 2014. 
There will be two releases before that: *0.9.8* will be beta with frozen API and store format. 
*0.9.9* will be release candidate without some documentation. There will be 4 week period between all releases. 

I [left behind](https://github.com/jankotek/mapdb/issues?labels=after+1.0) some features which I do not think are 
crucial for 1.0 release. Those should be implemented in 1.x releases:

 * [Compaction for append-only store](https://github.com/jankotek/MapDB/issues/98). Without this append-only 
 store is practically useless, since it consumes too much space. 
 
 * [Parallel transactions in TxMaker are slow](https://github.com/jankotek/MapDB/issues/221). Current 
  `TxMaker` version uses global lock while commit is in progress, so performance sucks. 
 
 * [BTreeMap does not release space after delete](https://github.com/jankotek/MapDB/issues/97). 
 This is trade-off for lock free algorithm. Solution is on-line compaction which is not written yet.
 
Business
============
My savings are shrinking, so I will have to figure out business model and monetize MapDB somehow. 
Short term priority is massive user base, which I might convert into support contracts and
consulting services. 

BTW: I will be available for hire in a few weeks. <a href="mailto:jan@kotek.net">Drop me a line</a> if you 
like MapDB and want some help. 

There are [some improvements](https://github.com/jankotek/mapdb/issues?labels=after+1.0)
which I will (probably) do in future for free. I have a lot of ideas, but those 
require investment beyond my current capability. So I have to figure out finances
before MapDB moves significantly beyond 1.0 release. 

There are ways which would allow me to continue on MapDB full time (kickstarter, funding, donations). 
Slower option is to provide consulting and work on MapDB part-time. 
And the third option is to sell enhanced commercial version. 
In any case I factored planned improvements into current design, so there should be no breaking changes in the future. 


Future plans
============

.NET port
----------
CLI platform is similar to Java. It has locks and memory mapped files. So MapDB 
port to CLI should be straightforward job. 


Master-slave replication
-------------------------
Replication with single writer and multiple replicas. Master could be swapped while 
running. Pretty much similar to Redis or Mysql replication. 

Parallel collections (fork-join)
---------------------------
MapDB collection are huge So it would be good to parallelize collections 
operations . There is similar [framework in Scala](http://docs.scala-lang.org/overviews/parallel-collections/overview.html). 
Also Java8 brings [Parallel Stream](http://docs.oracle.com/javase/tutorial/collections/streams/parallelism.html)
so MapDB would just implement API included in JRE. 

This would include:

 * reduce jobs such as count, sum, category
 * filter (or find)
 * copy collection into another collection with conversion
 * parallel join and zip
 
Stream implementation for Map-Reduce
-------------------------------------
Map-reduce jobs running on replicas. There are some similarities between fork-join 
and map-reduce, and no other DB provides seamless migration between those 
two. User could upgrade from single threaded to  parallel or clustered 
implementation without changing API, all would implement Parallel Streams 
which are part of JRE. 

Complete rewrite MapDB into Scala and Java 8
--------------------------------------------------
Right now MapDB uses simple composite locking. It is great, but probably does 
not scale beyond 8 cores. Concurrent library in Java 8 brings number of 
improvements (locks, collections..). Also Java is not best language for 
writing complex concurrent code. 

So I think complete rewrite in Scala (or Kotlin) and Java8 would push MapDB to utilize 32+ 
cores.

Asynchronous version
----------------------
Asynchronous web containers replaces threads with reactive programming based on 
futures or actors.  Async web container usually handles huge number of 
parallel connections. 

But those webservers usually serve data from memory. Using db is hard since 
threads are not available, and DB can not execute blocking operations such as 
read or write. MapDB could be rewritten to use futures on top of 
[AsynchronousFileChannel](http://openjdk.java.net/projects/nio/javadoc/java/nio/channels/AsynchronousFileChannel.html). 
First read-only milestone should be simple.
