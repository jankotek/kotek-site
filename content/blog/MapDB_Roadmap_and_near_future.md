+++
title = "MapDB Roadmap and near future"
template = "page.html"
description = "MapDB 1.0.0, the first stable version, was released last week. Some people tweeted \"Christmas came early\". For me it is the culmination of 5 years work. Lets open another chapter and have a look at MapDB in the near future."
path = "blog/MapDB_Roadmap_and_near_future"
date = 2014-05-14
[extra]
render_title = false
+++

MapDB Roadmap and near future
============================

MapDB 1.0.0, the first stable version, was released last week. Some people tweeted "Christmas came early". For me it is the culmination of 5 years work. Lets open another chapter and have a look at MapDB in the near future.

<!-- more -->
  
Open-source projects such as MapDB usually face two challenges: First funding: this is solved thanks to CodeFutures, which generously sponsors the MapDB development. CodeFutures will also help me to better assist paying customers. So funds wise MapDB is secure.

Then there is the vision and future direction of the project. I think MapDB is nearly perfect and it should stay as it is. There will be a lot of improvements, but those can be added without breaking anything. There will also be a lot of innovations around MapDB, but that will be done in separate projects. I have become a huge fan of Doug Lea and his work on  [Java Concurrency Framework](http://gee.cs.oswego.edu/dl/concurrency-interest/) and MapDB will evolve in a similar way.

Versioning and long term support
---------------------------------
My hope is that MapDB will become a de-facto standard database engine for Java. For that, it needs predictable releases and long term support.   

MapDB versioning follows a simple convention: *major.minor.maintenance*. Any major version marks storage format and API. Any minor version introduces new features, but keeps the backward compatibility with the existing features. Maintenance release contains only bugfixes and should not change its behaviour unless it fixes a bug. 

I see no reason for new major release, which would break backward compatibility, for next few years.   

A minor version with new features should be released every three months. This minor release will receive bug-fixes for three months until a new minor version is out. Every twelve months one release becomes Long Term  Supported release (LTS) and will receive bug-fixes for two years. The next LTS will have compatible API and storage format, but some new features could in theory cause problems to existing code.   

So MapDB users will get a production worthy release every year. LTS release will receive bug fixes for 24 months, giving plenty of time to upgrade to the new LTS version. Even longer support is possible as part of contract, or for high profile OS projects.

Right now the Long Term Support release is 1.0 and it will be supported until May 2016 when 1.8 will be released. 

   
Road map
--------------
Work already started on 1.1 branch, but right now I have these priorities:

 * Finish documentation and website.
   
 * Create a few sample applications with Wikipedia and OpenStreetMaps snapshots 
 
 * Automate release acceptance testing. Right now I have thousands of manually run tests, those runs for days and create several terabytes of data.  
  
 * Setup benchmarks and automated performance regression test.  
  
 
Minor release should be out every three months. Here is the road map for the next year until the next LTS release 1.4:
  
**1.1** - Will introduce Append-Only-Files store with native snapshots. It will also improve `TxMaker` concurrent performance by grouping multiple commits into single file-sync. Right now MapDB has very limited speed with multiple concurrent transactions and this release will fix it. Bugs: [#241](https://github.com/jankotek/MapDB/issues/241), [#98](https://github.com/jankotek/MapDB/issues/98), [#221](https://github.com/jankotek/MapDB/issues/221). 

**1.2** - This should introduce independent backup format. It will allow you to dump content of database into a single file. Also `BTreeMap` will get some updates, mainly online compaction, faster iteration in reverse order and per-node aggregates (counted btrees). Bugs: [#283](https://github.com/jankotek/MapDB/issues/283), [#97](https://github.com/jankotek/MapDB/issues/97) and  [#207](https://github.com/jankotek/MapDB/issues/207)

**1.3** - Will bring major update into existing stores. `StoreDirect` and `StoreWAL` will get native snapshots in form of copy-on-write and incremental backups. It will make MapDB much faster and more usable for many scenarios.  Bugs: [#200](https://github.com/jankotek/MapDB/issues/200)

**1.4** - Will add new collections. HTreeMap will be refactored to provide separate HTree structure, an indexed sparse array. We will get alternative for ArrayList which fully implements BlockingDequeue. There will also be compressed BitSet to support large bloom filters. And perhaps HugeString and HugeBlob. 


Side projects
---------------

There are a number of exiting features, which cannot be added into the core MapDB for various reasons: 

For example `sun.misc.Unsafe` allows direct memory manipulation which may crash JVM. Also it is not a documented part of Java and does not run on Android. But it gives about 10% performance increase to in-memory database. 
 
Another example is Snappy compression from Google. But it cannot be added into core MapDB, because it is a large library with dependency on JNI libraries or Unsafe. MapDB uses LZW compression which is almost as good, but only has 20 lines of code.
  
MapDB is highly modular, so this type of features can be added as a separate project. [MapDB-Snappy](https://github.com/jankotek/mapdb-snappy) is already out, MapDB-Unsafe is almost finished. Other things in backlog are Graph-API, Network Interface, Redis reimplementation, SHA256 encryption and so on. I would like to publish a similar project  every two weeks. 
   

Future goals
---------------
  
Right now my major goals for MapDB are:

 * Improve concurrent performance scalability on multiple CPU cores. Thanks to CodeFutures I now have physical 24 CPU machine and I want almost linear scalability on this hardware. That should keep me busy for another decade :-)
 
 * Investigate operating system settings and its impact on performance. MapDB uses memory-mapped files and it heavily depends on OS memory management and file system settings. 
     
 * Implement Java 8 streams parallel operations using Fork-Join Framework
