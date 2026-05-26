+++
title = "MapDB Future"
template = "page.html"
description = "MapDB 0.9.x was released a few weeks ago. Now that the project enters usable alpha phase, is time to talk about the future."
path = "blog/MapDB_Future"
date = 2013-04-23
[extra]
render_title = false
+++

MapDB Future
=============
MapDB 0.9.x was released a few weeks ago. Now that the project enters <i>usable alpha phase</i>, is time to talk about the future.

<!-- more --> 

What is next
--------------
MapDB 0.9 branch is a stepping stone to the stable 1.0 release. It will take some time before MapDB is production ready. Obviously it is more important to fix bugs and write documentation. But I also need to finish and document disk-store format. And there are also 120 tasks on my TODO list. I expect MapDB 1.0 to be released in about 10 months (February 2014).
 
MapDB development is test driven. Now I would normally start writing unit tests to catch most corner case bugs. But I simply do not have the time to do it for a hobby project. So for now I will write an acceptance stress test to catch most of the concurrency issues. This test will run for about two weeks, create a few terabytes of data and give reasonable confidence that the release is stable. Obviously it will be in separate maven project.
 
Community growth is another problem. Just making the community larger is simple; a few hyped articles on Hacker News and popularity would sky-rocket. The problem is the additional workload that a larger community brings. Right now I get about 50 emails per week; I think I could handle about 200, that is not much space for growth. So for now it is not my priority to attract new users. That is why MapDB does not have performance benchmarks and other stuff usually found on commercial DBs.
 
I need to improve MapDB in many ways before it hits broader adoption. It must be stable enough so I do not get flooded with bug reports. Also a good way to decrease the number of support emails is to improve usability; first by documentation and examples and second by clear error messages, IndexOutOfBoundsException is never a good warning that you used the wrong serializer. Third are the hints produced by a logger if the MapDB is used the wrong way.

10 to the 10 in 10
-----------------------
Until now the MapDB goal was to be *‘the fastest db engine written in pure Java’*. We may debate if this has been achieved, but for me, my quest for perfection was successful.  So now what? MapDB is very flexible and it could be steered in any direction. But my time is limited and I would prefer an area where it can succeed without years of development. This rules out ultra-durable storage, highly-available clustering and various enterprise deployments. For most people MapDB is just a ‘cute db’ not suitable for real deployment and it can take years before it is recognized as a reliable DB, if at all.
 
So I need a scenario where MapDB does not have to pass through a committee review. I think the best direction for MapDB is to be a fast analytical data engine, an alternative to in-memory processing, something like a data fork-lift for feeding Hadoop or Cassandra.
 
The next goal for MapDB development is **10 to the 10 in 10**. It means processing 10 000 000 000 records (10^10) in ten hours on an ordinary workstation. MapDB should enable any programmer to process huge data sets on their laptop. I already did something similar with [Healpix-RangeSet](https://code.google.com/p/healpix-rangeset/) in Astronomy.
 
Right now the goal is to import 10^10 items overnight. MapDB can already import huge BTree if the keys are presorted. For unsorted keys, the current practical limit is around 250 000 000 items. Te solution for data imports is [Data Pump]( https://github.com/jankotek/MapDB/issues/94), it will presort keys and construct BTree by layers in linear time.
 
Latter I will implement [Parallel Collections](https://github.com/jankotek/MapDB/issues/101) to handle updates and queries over huge datasets. MapDB will get heavily integrated with Fork-Join framework to parallelize most of its operation (such as parallel compaction). There are also small performance improvements to be done, such as spreading a load across multiple hard-drives.

I have more plans open for discussion, you may find them on [Github under 'discus' tag](https://github.com/jankotek/mapdb/issues?labels=discus&page=1&sort=updated&state=open).
 
The DB engine excuse
---------------------
MapDB (aka JDBM4) development started exactly one year ago.  Originally I planned it would finish in 6 months. However, I spend a lot of time investigating complex storage algorithms and various concurrency libraries. It turned to be a huge waste of time and dead end. The current MapDB uses very basic algorithms and a few simple concurrency tricks.
 
So the project was delayed and in some troubles. My wife was pregnant, the due date was approaching fast and my willingness to work on MapDB dropped below zero. Luckily for you, my baby girl sleeps for 10 hours during night without waking up, so I have some time for my hobbies.
 
Why this rant? On the mailing list I may sound brief (perhaps impolite) and you should know why. I would love to have a chat, discuss frameworks and algorithms, perhaps even get a free beer, but it is simply not possible. Also I wasted a huge time on LSM trees and other ‘fancy algorithms’ highly recommended by others. This made me a bit skeptical.
 
So right now my only goal is to release MapDB 1.0. This means stabilizing and extending MapDB on its current form. To make sure it happens I have to refuse most of the abstract suggestions (this does not apply to concrete code reviews and patches!!). I don’t want to be negative, so I will just use the following excuse: *‘MapDB is a db engine, this stuff should be in an external library’*. But in reality it just means I have no time to investigate (or even evaluate) your suggestion. If you think your stuff is viable, go ahead develop the prototype and benchmarks, it may eventually get integrated.
 
Help me!
---------
As I wrote MapDB as just a hobby project, there is no business plan, no investors and no commercial support. There is only one dude hacking on evenings who may walk away anytime. So if you are using MapDB, I would strongly recommend you contributed to in some form, to make sure this project survives.

MapDB has a very small code base. Without the unit tests, there are only 11 000 lines of production code. One could comfortably read it from top to bottom in one weekend. You can make real impact on this project in a very short time.
 
Also there are many tasks which do not even require knowledge of MapDB code. By choosing to do one of those, you will save me time, so I can work on core issues. Those are:
 
* **Performance benchmarks**. MapDB performance should be compared to its competitors (Berkeley DB JE, LevelDB, Persistit…). But it is time consuming (Berkeley has really cryptic API) and tricky to implement right (fair to all dbs).  Also as a MapDB author, I am not neutral and any benchmark coming from me will always be questionable.

* **Proof reading**. Soon I will scribble a lot of documentation in very short time. English is not my primary language so the initial version will be horrible, more likely brain-dump than documentation.  I need someone to decipher it and make it readable. 

* **Graph API and other libraries**. MapDB needs some supporting libraries to attract new users. Implementing those on top of MapDB collections should be relatively simple. Examples are [Redis reimplementation](https://github.com/jankotek/MapDB/issues/92)  or [Graph API](https://github.com/jankotek/MapDB/issues/96).

* **Testing on exotic platforms**. MapDB supports a large variety of platforms from Android phones, corporate laptops with Windows XP to beefy super-node computers. Java NIO performance depends on OS and various settings. We need to collect the best practices for most of those platforms.

* **Donating Hardware time**. MapDB acceptance test runs for one week. It is becoming problematic to finish pre-release testing on my home workstation. I could use a remote machine where I could do continuous integration.  Also I would love to test MapDB on a machine with 128GB RAM and 16 cores.
