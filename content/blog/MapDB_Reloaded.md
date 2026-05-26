+++
title = "MapDB Reloaded"
template = "page.html"
description = "Last month I wrote about the future of MapDB. It was not very optimistic. MapDB is my hobby project and the time I could give it is severely limited. This led to some absurd situations: despite having a very fast db-engine I would not publish any performance benchmarks. I also discouraged possible users so I would not have to deal with support emails."
path = "blog/MapDB_Reloaded"
date = 2013-06-19
[extra]
render_title = false
+++

MapDB Reloaded
==============

Last month I wrote about [the future of MapDB](/blog/MapDB_Future/). It was not very optimistic. MapDB is my hobby project and the time I could give it is severely limited. This led to some absurd situations: despite having a very fast db-engine I would not publish any performance benchmarks. I also discouraged possible users so I would not have to deal with support emails.

<!-- more -->

Years ago I revived the JDBM project (former MapDB name) with the hope that a community of developers would grow around it. This idea has failed. There is a small stream of bug reports and patches, but four years latter I am still the only developer.  Users do not send patches, but ask for commercial support. And when I ask a commercial company to support open source project I usually get 'just' a job offer instead. It is simply not possible to fully develop a project like MapDB as a hobby. 

MapDB has been around for more than a decade. The current version is in a league of its own in terms of speed, usability and simplicity. And I think it deserves a fair chance to succeed.  My work on MapDB was always about taking the harder choice. I stripped internal classes to bones to reduce GC trashing. I removed block layer to reach zero-copy. And finally I rewrote the whole dam thing to introduce fine grained concurrency. So the current situation is just another hard choice to make and the answer is obvious. 

Last week I finished in my day job and now I work on MapDB full-time. Founding a startup with young family is hard, but we have enough savings for one year runway. My short-term plan is to release stable MapDB 1.0, charge for user support and do consulting. My long-term plan is to develop and sell MapDB tooling such as profiler, reporting and other stuff. 

There is an obvious question: Will the license change from business-friendly Apache License to something more restrictive? The answer is no. I believe that MapDB has good chance to become the de facto standard Java storage engine. For that it needs permissive license and even LGPL could ruin its chances. Also the dual licensing (GPL+commercial) business model would put me into same ring with fearsome competitors such as Oracle.

So now what? Right now MapDB stinks as a half-baked hobby project. So for the next three months I will sprint to improve it. The quality and number of tests will raise.  It will get a proper website and documentation. The usability and error handling will improve (even if this means small performance loss). And it will get better marketing with benchmarks, blog posts and twitter. 

Then it will be time to spread the word. I will start a number of subproject to drive MapDB adoption; stuff like Graph API, Ehcache backend, Redis protocol compatible server and so on. MapDB can also serve as an engine for other databases, so for a start I will patch Cassandra and Lucene to use MapDB backend. 

On side I will create a consultancy business. MapDB is basically an alternative memory model for Java. And it makes possible to rewrite the data-model to use off-heap (or SSD) storage without sacrificing much performance. There are similar solutions, but those offer only primitive put/get interface. MapDB offers richer interface, more flexibility and much better performance.

Backwards compatibility (API and storage format) is very important for enterprise dbs. A stable MapDB 1.0 will be released by 1Q 2014. This version could be around for decades, so storage format and API must be done right. There will be some changes to make the MapDB components less coupled, and the storage format more extendable. Parts such as serialization may be moved into a separate project. The current 0.9 branch will be supported until 2Q 2014, a few months after 1.0 release. 

Fasten Your Seatbelts and Enjoy the Ride! 


edit: fixed grammar and typos
