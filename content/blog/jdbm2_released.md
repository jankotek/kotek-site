+++
title = "JDBM2 released"
template = "page.html"
description = "I am proud to announce stable release of JDBM2 key-value database. It is similar to BerkleyDB Java Edition, but is free as beer and under Apache 2 license. JDBM2 provides 'java.util.Map' stored on disk."
path = "blog/jdbm2_released"
date = 2010-12-19
[extra]
render_title = false
+++

JDBM2 released
======
I am proud to announce stable release of [JDBM2](http://googlecode.com/p/jdbm2)  key-value database. It is similar to BerkleyDB Java Edition, but is free as beer and under Apache 2 license. JDBM2 provides 'java.util.Map' stored on disk.

<!-- more --> 

Unlike others key-value databases JDBM2 really focuses on simplicity. It have transactions, btree+hash indexes, soft object instance cache and space efficient serialization. All this packed into 140 KB jar without any dependencies. 

JDBM is old project, it started in 2000. Version 1.0 was released in 2005 and was stable release for next five years. This version started 8 months ago, and contains many improvements. Huge thanks to original JDBM 1 developers: Alex Boisvert, Bryan Thompson, Kevin Day, Elias Ross and Cees de Groot.

JDBM2 is fully **transactional**. Changes can be reverted before commit. If program crashes before commit, all changes are rolled back. JDBM2 have only single transactions, so there is no locking and concurrent modifications. 

**Space efficiency** was huge priority in JDBM2 development. There are dozens of tricks for better storage use. For example BTrees have delta key compression, numbers are packed, record offset are minimalized. There is also space efficient serialization for most java.util.* and java.lang.* classes. On top JDBM2 have on demand defragmentation. 

JDBM2 also have **soft object instance cache**. All fetched object are cached using soft reference. If free heap memory runs low, garbage collector can dispose cached objects. Big care was taken to keep cache overhead low.

**java.util.Map view**. Original JDBM has two indexes: BTree and Hash with custom API. JDBM2 adds java.util.SortedMap and java.util.HashMap views on top. There are also secondary maps which corresponds to foreign keys from SQL.

There are dozens of other improvements. Most notably number of object instances created inside JDBM2 is now very small, to reduce GC trashing. 

JDBM2 was developed as embedded storage for astronomical desktop application. It is used to store millions of stars in display them in real time. Hopefully you find it useful same way author did. 

[JDBM2 home page](http://googlecode.com/p/jdbm2)
