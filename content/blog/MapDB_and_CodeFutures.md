+++
title = "CodeFutures: the new MapDB home"
template = "page.html"
description = "MapDB was a hobby project for almost 12 years (under the name JDBM). Last year I quit my daily job and started on MapDB full time. The plan was to finish MapDB 1.0 and build a consultancy business around it. I also wanted to work from home and spend more time with my family."
path = "blog/MapDB_and_CodeFutures"
date = 2014-01-21
[extra]
render_title = false
+++

CodeFutures: the new MapDB home
=============
[MapDB](http://www.mapdb.org) was a hobby project for almost 12 years (under the
name JDBM). Last year I quit my daily job and started on MapDB full time. The plan
was to finish MapDB 1.0 and build a consultancy business around it. I also wanted
to work from home and spend more time with my family.

<!-- more -->

This worked surprisingly well. MapDB now has enterprise grade features, such as ACID transactions, snapshots, entry expiration and an append-only store. Users already using MapDB in production. So turning MapDB into sustainable business is plausible.

Work on the database engine is very rewarding, if not addictive. It brings the elegance of mathematics, combined with the bonus of happy users and good pay. But running a business while hacking MapDB is challenging, and the productivity suffers while switching between those two. Of course I will spare you details about start-up financing, etc. 

In short, the current situation is about two choices:

Keeping MapDB self-funded requires a lot of time on the business side of things. It slows down the development and causes productivity loss.

Funding from an investor would restrict a free-with-no-strings-attached Apache license. It would also mean specializing MapDB for one particular niche.

As you may know, I want to turn MapDB into the de-facto standard database engine for Java.
For that I need lot of time on the technical side with no licensing restrictions.

The author of Redis had a 
[similar dilemma](http://oldblog.antirez.com/post/vmware-the-new-redis-home.html)
 just three years ago.

Fortunately there is a third option.

CodeFutures
--------------------------------
There were a number of people and companies who supported and influenced
MapDB over time. One of the technical discussions led to an offer, which I took.
[CodeFutures](http://www.codefutures.com) are using MapDB (and JDBM3)
in their products. They need a good database engine and also understand
the benefits of open-source. So most of my new job description is to maintain
and develop MapDB. The CodeFutures team also have a set of skills which complements MapDB: sharding, clustering, query parsers and optimizers, to name a few.

And most important, the MapDB project will keep its independence as a database engine under Apache License. This is a best fit situation for my vision of MapDB as a universal database engine.

So what is changing for the MapDB users? Well, not much, apart from me having more time for development. A stable MapDB 1.0 released will be released soon, as planned. Thanks to CodeFutures I already have ideas for new stores and collections, so MapDB 1.1 will follow some time soon. CodeFutures will take care of the commercial side, such as negotiating support contracts, assisting with more support and consulting resources, and other matters.
