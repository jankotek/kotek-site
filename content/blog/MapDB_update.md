+++
title = "MapDB 2.0 update"
template = "page.html"
description = "To begin with, there is a small notification of changes. From now on I am moving the MapDB related posts to a new blog at mapdb.org. Here is new RSS. This blog will be used for my interests outside MapDB (most likely it will stay empty)."
path = "blog/MapDB_update"
date = 2015-09-25
[extra]
render_title = false
+++

MapDB 2.0 update
================

To begin with, there is a small notification of changes. From now on I am moving the MapDB related posts to a [new blog](http://www.mapdb.org/blog.html) at mapdb.org. Here is new [RSS](http://www.mapdb.org/news.xml). This blog will be used for my interests outside MapDB (most likely it will stay empty).

<!-- more --> 

TL;DR I am moving many features from 2.1 to 2.0. I am did major changes in storage to fix a data corruption issue and there is going to be storage a  format change. A stable 2.0 version will be released by late October and will most likely get long-term-support. 

Business
---------------
You probably know that I lost my sponsor a few months ago. He sponsored MapDB for a very long time, had a lot of understanding for the MapDB open source nature,  and I am very grateful for that. But business plans change, and it would be very hard to scale up MapDB business model .  So far I supplemented part of my income by consulting, so there are no financial issues for the MapDB project.

The consulting business picked up. I already have had a few gigs and more are lined up. I made a trip to the Canary Wharf. A pharmaceutical company is using MapDB to crossmatch DNA. A huge hardware company wants to use MapDB on a new type of memory.  Others are using it for bitcoin analysis and public transportation planning and so on. 

I spend a lot of time working on a stable release, but the consulting I do already pays for my living expenses. I will be fully allocated by the time stable 2.0 is released. I was worried about administrative overhead, but this is ok. My customers have great need for my services and paper-work is quickly resolved. I spend minimal time on negotiation, estimates and advertising, and that seems to work just fine.

Company
-------------------------
For the foreseeable future I have decided to keep MapDB as an one-man show (not that I have more options). For the users it is actually good news, because I have kept some ideas for the commercial version. But I have no capacity to maintain a closed source branch, so I decided to include everything into a free Apache licensed version. Open-source software requires less marketing, is easier to fix and gets more bug reports. 

That includes:

- Parallel Java8 Streams. It can execute operations such as filter, find etc. in parallel with many streams. `HTreeMap` and `BTreeMap` could easily have billions of items, and allow easy slicing, so this will be pretty powerful. 

- Disruptor Storage Engine. It has core (memory allocator) pinned to single thread and separated by spin queues from other threads. In theory it scales linearly up-to 32 cores and is pretty fast. There is a huge potential when grouped with Actors.

- Uninterrupted operation, such as background incremental backups, background compaction…

- Parallel version of MapDB tasks: multithreaded recovery, multithreaded  compaction, multithreaded cache eviction…

- Unsafe optimizations

- Various sharding methods to improve concurrency and uninterrupted operation. 

- Stress tests and acceptance tests (they have a huge value for me)

- Network servers, IPC...

- Enterprise integration, monitoring and logging, such as JMX, JTA and Spring integration


My priority for the near future is to streamline business and automate most tasks. I am going to hire an administrative assistant. I started using semi-automated time tracking software. And I am going to  move most  CPU intensive tasks into cloud. 

I also adopted new development routine and tools, which suits me much better. I will write about that a bit latter.

Storage update
-------------------------
Current storage engine has two major problems: First its locking sequence is wrong and does not allow background compaction and backups (without blocking write operations). I was planning to fix this in 2.1. Secondly I discovered Write Ahead Log corruption issue. 

After some estimates I decided to do major update as it is easier than just quick fix. It took three months to write current storage, major update will take 2 weeks, about 80% of that for tests. Concurrent storage is hard to do right, with new code I can be a way more paranoid about handling corner cases. 

I also added a few improvements. New version will be faster, use less space and will reuse free space better. Bad news is that this will change storage format. 

There is a new lock sequence, which will allow to make writes and commits while underlying storage is being modified by compaction. Rather than using random record locks based on hash, I will lock entire index table segments. That should speedup compaction and improve its parallel scalability.

Also I am writing new tools to analyze storage. It will detect various forms of data corruption, such as cyclic links, overlapping records, rogue pointers etc. Every storage byte is now accounted for. This will allow me to detect data corruption early, and it will also allow me to fix smaller issues such as storage space leaks. 

And there is binary equality. Current storage format has three different implementations (direct, cached, WAL). All have small differences, so they produce slightly different binary files, but valid within specification. Bbinary difference prevents me from comparing their results. New implementations are strictly equal in their output. The same sequence of operations always produce files with identical contents. This allows me to compare different implementations and catch bugs earlier. 

And finally small bonus. I decide to move Write Ahead Log into independent class and make it reusable. `StoreWA`L and `StoreAppend` will both share this component. This will simplify crash protection and crash recovery a lot, reducing code and testing. WAL will also be reusable outside MapDB, so other projects will be able to use it. 

Timeline
-------------

2.0-beta8 with new storage format should be out by end of September. After that I will concentrate on clean up TODOs while stress tests are working. October will see mostly small performance improvements and bug-fixes. I will also finalize major features such as background compaction and backups. 

Stable 2.0 should be out at end of October.
