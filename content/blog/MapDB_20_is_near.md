+++
title = "MapDB 2 is near"
template = "page.html"
description = "Format and API freeze for MapDB 2.0 is just a few weeks away. I did not write much about the new generation of MapDB (aka JDBM) and it is time to fix that."
path = "blog/MapDB_20_is_near"
date = 2015-06-16
[extra]
render_title = false
+++

MapDB 2 is near
=====================

Format and API freeze for MapDB 2.0 is just a few weeks away.
I did not write much about the new generation of MapDB (aka JDBM) and it is time to fix that.

<!-- more -->

So first lets talk about dates. Right now there is MapDB 2.0-alpha3. I think it has good quality
for development release. It also addresses most of my TODOs, so its format should not change much
(except append-only store).

Before I commit to freezing format and API, I need to review bug reports and some notes.
Also there are some stress test which take some time to run.
So **2.0-beta1** should be released by the **end of June**.

Once beta is out MapDB storage format and API should remain stable,
so beta and stable release should share the same storage format. 
However, it is possible that some bug-fix might require storage format change (this was the case with 1.0 beta).
In that case, the data migration tool designed for 1.0 users, will support the 2.0 beta format as well.

After beta1 is out, there will be bug-fixing and a few beta releases.
I would like to publish a new release every two weeks.
Once there are no major issues in 2.0 branch, the **stable MapDB 2.0** gets released, 
most likely in **September or October**.

MapDB 2.0 release prefers stability over speed.
So the next 2.1 version will contains mostly speed improvements, which did not make it into 2.0 release.
There will be also some goodies from Java 8 added into 2.1
I expect a stable **2.1** some time in **December 2015**.
2.1 will not contain storage format changes.

2.1 release will be **long-term-supported**. 
It will receive bug-fixes for a couple of years, even after newer versions are released
MapDB 2.0 will be supported for a couple of months after the 2.1 release, to give the user time to migrate.
MapDB 1.0 support expires on April 2016, but it might be extended if a stable 2.1 is not out yet.


New features in 2.0 release
-----------------------------

MapDB 1.0 was not bad, but it had some design issues. A big part of it was rewritten and redesigned.
There was a 30% code reduction in storage components. The new code is more compact, streamlined and more robust.

MapDB 2.0 brings several new features. Some of those are already in alpha/beta release,
others will be added before stable 2.0 is out.

The most important additions are the **bit-parity checksums** on pointers. When storage gets corrupted,
there is a 75% chance MapDB will throw an exception on the first read. This chance grows exponentially with the number of reads,
until it is almost certain. This is important to prevent sneaky data corruption,  which could go undetected
for a long time, just to manifest at a completely different place. 

Another important change are **specialized BTree serializers**. It reduces the BTree read amplification several times,
so BTreeMap has now much better performance. It is even faster than `java.util.TreeMap`. 
The trick is to use specialized keys in BTree Dir nodes. 
`Long[]` is represented as `long[]`, `String[]` as single `byte[]` and so on. 
Memory consumption is down several times, and doing binary search on long[] is very CPU cache friendly.
We will hear about this feature a lot in the near future.


There is a new '**heap mode**' which does not use serialization, but stores all data in deserialized form on heap.
In this mode MapDB consistently matches `java.util` collections performance, while it fits 4x more data into the same memory.
The trade-off is that MapDB is limited by JVM garbage collector, but no storage compaction is needed, GC does it for us.

`StoreDirect` now has **native snapshots** with copy-on-write.
The old version would make a copy of the old data on update, and store it on heap, with a huge memory overhead.
This reduces the overhead of snapshots and it improves  the performance with concurrent transactions.  

We finally got decent **append-only store** with background compaction .
MapDB now can emulate LSM trees found in several other databases. 
  
Write cache and Asynchronous Writes were merged into the storage layer. Now it has lower overhead and brings more benefits. 
Also it makes a transaction with Write-Ahead-Log faster. 

Another great news is less **lock contention** in MapDB 2.0. O
The old version had hierarchy of components, each component with its own locking.
This was solved by redesigning the component hierarchy.
Now there are less locks and less memory barriers, so MapDB should scale better on multiple cores.

Executor framework was introduced. MapDB now does not start its own threads, but uses `ExecutorService` provided by the user.
Now MapDB can use asynchronous operations even in restricted environments such as J2EE containers or Google Web Services. 
Also there are more options, for example cache eviction can run in multiple background threads. 

There are changes in **compaction**. It is now **multi-threaded** and can run much faster 
due to lower IO latencies. Also compaction can now run in parallel with updates and commits. 
There is no need to stop-the-world while compaction is running. 

MapDB has become much more **user friendly**. 
There are several log warnings to give user hints on better configuration options.
We are less strict, so for example key serializers are no longer required to be serializable. 
Some configuration options are no longer needed. For example correct 
`Hasher` and `BTreeKeySerializer` are used automatically if the correct Key Serializer is provided.

Less obvious but a fairly important change is in serializers. Before it was just conversion from/to binary form.
But now the data can be represented in intermediate compact form and Serializers are used 
to interpret them (equals, compare, hash code). 
For example UUID[] (array of 128bit numbers) can be represented as long[] in BTree nodes. 
This greatly reduces memory overhead and improves performance     	
	
I finally embraced `sun.misc.Unsafe` and added it into core distribution. Current usage is fairly
conservative and only brings 10% performance benefit. `Unsafe` is
completely optional and we will produce flavour without it, so MapDB can run on Dalvik and other JVMs.

MapDB 2.0 will use *code preprocessor* and will come in several flavours. For example detail logging is useful,
but ads some overhead. So the default version will be compiled without it, but one can always replace it with
`mapdb-core-logging.jar`, which is compiled with logging. Other flavours solve dependency on Unsafe, Java 6/7 compatibility etc.    
	
2.1 release
----------------------

Release 2.1 will come a few months after 2.0. 
Storage and API format will remain compatible with 2.0.
It will mainly contain speed improvements.
This version will also have long-term-support for a couple of years. It will receive bug-fixes even
after newer versions are released.

I finally fully embraced and understood `sun.misc.Unsafe`. When used correctly it can bring huge
performance improvements, for example LZV decompression is 3x faster with Unsafe.
2.0 already contains basic and conservative support for Unsafe (about 10% performance improvement).
MapDB 2.1 will have all those tricky optimizations.

There are going to be some API changes.
MapDB 2.0 has many deprecated methods, to keep compatibility with 1.0 branch,
so classes `DBMaker` and `DB` are mostly working with existing code.
But all deprecated methods will be removed in 2.1

Java 8 added functional programming  to Java Collections.
I like those, so MapDB 2.1 will get top integration with Streams and Spliterators.
For that MapDB 2.0 will depend on Java 8. 
Support for Java 6,7 and Android will be provided in separate flavour, generated by code preprocessor. 

A  real game changer for MapDB could be parallel streams added in Java 8.
Our collections could easily have 1e10 items, and parallel processing
(such as find, filter, reduce...), which would be a great advantage.
`Spliterator` is a fairly simple idea and should be simple to implement.
But the key is to implement it efficiently, inside MapDB locking the mechanism with Data Pump integration.

Another reason for requiring Java 8 is `StampedLock`. MapDB 2.0 reduced the number
of locks and locking contention. But for more concurrency improvements  I need
new low level features added in Java 8.

And finally MapDB 2.1 will improve the memory allocator. In version 2.0 it is fairly primitive, but stable.
MapDB 2.1 will get a more advanced allocator, which will better manage and reuse space. 
That should greatly reduce fragmentation after frequent updates. 
Full compaction will be still needed, but less frequently.

Commercial support
---------------------

MapDB is generously sponsored by CodeFutures corporation. Their main product is 
[AgilData](http://codefutures.com/agildata/). 
A distributed data platform which is similar to MapDB in terms of speed and flexibility.
We already provide  consulting for MapDB (remote and onsite).
After MapDB 2.0 gets reasonably stable we will also
provide support subscription and other services for MapDB.

For practical reasons commercial support will be limited to Java 7 and 8 running on 64bit Linux
(there is no problem to include other combinations if the customer requires it).
Other platforms (Android, Windows, Java6, 32bit...) should work fine,
but will only get basic testing on a best-effort basis.
A full test suite takes several weeks to run on a single platform/JVM combination,
and we can fully test all possible combinations.

Side projects
-----------------

In the future the core will be stable and most development will happen in side projects.
I see it as a way to promote and expand the MapDB ecosystem. Right now there are following projects in pipeline
(in order of priority)

Import and export tool. This will take all collections in MapDB store and save their content into single text file.
It can also create a new MapDB store from an existing text file.
It is critical as a data migration tool for MapDB 1.0 users. It uses
XStream framework to serialize data into JSON human readable text format. 1TB of text data is not very practical and
MapDB has more efficient binary incremental backups,
but the text format is independent and parse-able outside MapDB or Java.

Redis is widely used for caching. MapDB could offer similar speed with concurrent scalability. So this project
will implement Redis Server protocol in pure-java with MapDB as backend. There will also be an embedded mode which will
use patched Jedis driver to invoke MapDB directly. MapDB should be a drop-in replacement for Redis.

Another standard is JCache. It replaces EZCache and other proprietary caching solutions with standardized caching API.
The initial investigation shows it will be simple enough to implement this API.

Hazelcast offers distributed Maps, Locks etc. Its technology is easy to use, but has many technical limitations.
One of them is GC overhead as all the data on nodes are stored on-heap. This could be solved by MapDB storage backend,
which would store data outside the heap. We already have a public prototype and it works great.

And finally MapDB should get graph API. There is pending TinkerPop implementation and I would like to add some
data structures into core, to make graphing easier.
