+++
title = "MapDB and the road ahead"
template = "page.html"
description = "Five months ago I left my regular job and started on MapDB full time. I have been quiet since, so it is time to refresh my plans with MapDB."
path = "blog/MapDB_and_the_road_ahead"
date = 2013-09-25
[extra]
render_title = false
+++


MapDB and the road ahead
======================

Five months ago  I left my regular job and [started on MapDB full time](/blog/MapDB_Reloaded/). 
I have been quiet since, so it is time to refresh my plans with MapDB.

<!-- more --> 


The last few months
-----------------
In order to understand the current situation, I will quote from a previous blog post: *Right now MapDB stinks as a half-baked hobby project. So for the next three months I will sprint to improve it.*

This turned to be more true than I would like to admit. MapDB (and JDBM) was carved as a simple hobby db engine and I took some shortcuts with its design. For example it was never meant as highly available engine, and would require periodic 'stop the world' compaction.  

I had to redesign core parts to address this. Recursive-free-stack-reallocation and other bugs were not easy to fix, but I managed somehow. Most of these solutions are still on paper. It will take a few months, before they are carved into code. 

The important thing for now is that the MapDB design is completed. The store format now is flexible and should allow long-term evolution without breaking changes. I also have blueprints and prototypes for future development (on-line compaction, native snapshots, incremental backups, replication..) 

Redesigning MapDB was very draining and it required most of my capacity. Now it is time to concentrate on more practical parts and actually deliver it. 


Towards a stable release
-------------------
Until now I treated MapDB as my hobby. I would pickup problem I like and work on it until satisfied. This is great for producing an elegant and almost perfect software. But delivering production ready software requires more coordinated approach. 

First I will make the MapDB development more transparent and predictable. Most of the design and bugs are still in my brain, but it should eventually be materialized into source code and Issue list, to get some feedback. We should also have periodic releases (3 weeks cycle) with predictable [roadmap](http://www.mapdb.org/roadmap.html). There is also documentation, I would like to produce a 50 page introduction build around code examples and use cases.

MapDB has 1589 unit tests, but it is still under-tested. So I am developing an extensive test suite. My inspiration is famous [SQLite test suite](https://www.sqlite.org/testing.html). This is challenging (for example there are no open-source smoke tests for Concurrent Maps) but I am making good progress. This suite also tests performance regressions. It will also ensure MapDB runs smoothly on all supported platforms (Android, Windows, OpenJDK..).

MapDB should have some community by the time the production-ready version is released. I am not very good at marketing and community management (JDBM2 and JDBM3 were disasters). I think the best 'technical' way is to integrate MapDB into various open-source projects as a database engine. This should give me legitimate cause to 'spam' the mailing lists. It also exposes MapDB to various usages and helps to find bugs early. The pilot project is  [Blueprints graph provider](https://github.com/jankotek/blueprints). So far this approach has been effective; the number of bugs and contributors sky-rocketed. 

Users will fiddle with various settings to achieve the best performance. For example how does `asyncFlushDelay()` affect performance under a highly concurrent load? A good answer is visualization and automation. I will run all scenarios with all configuration options (this may take a couple of weeks). The output of this will be a multi-dimensional matrix, which can be visualized by JavaScript or some other tool. 

I do not like performance benchmarks (and avoided them until now). However it is necessary for business. So there will be performance benchmarks comparing MapDB with its competitors (LevelDB, Berkeley DB JE, Persistit, EhCache and BigMemory GO. 

Changes before MapDB 1.0
-----------------------------------
MapDB 1.0 design is completed, however some features were not yet carved into code. This includes backups, 
better concurrency and so on. Please visit [Issue List](https://github.com/jankotek/mapdb/issues?sort=updated&state=open) and  [label missing](https://github.com/jankotek/mapdb/issues?labels=missing&page=1&sort=updated&state=open) to see the current state.


Beyond MapDB 1.0
-----------------
There are improvements which I could not add into MapDB 1.0. Some of them will be added in latter releases. For some others I will have to figure out funding. Checkout label [after 1.0](https://github.com/jankotek/mapdb/issues?labels=after+1.0&page=1&sort=updated&state=open) to see the list.

Software is often 'innovated away'. The new version removes important features and adds only cosmetic changes; eventually only a shadow of the original remains. But not here, I am building MapDB 1.0 to last for years or even decades. There will be improvements, but I will be very conservative in core questions (such as removing support for Java6). 

Another question is 'software bloat'. MapDB today is a fairly small and simple library. Excluding tests, it has a single package, 37 classes and 14KLOC. The compiled jar has only 300KB and the only dependency is Java 6. I believe it should stay this way. MapDB has extensible design and future staff (parallel collections, replication) will go into separate projects. 

I see the future of MapDB in a huge number of small improvements added over the span of many years.


The Startup
-----------
For now I provide consulting for MapDB. In about a year I will try an alternative model (donations, support fees, selling enhanced version).
