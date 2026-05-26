+++
title = "JDBM 3 is coming"
template = "page.html"
description = "A few weeks ago I started work on JDBM 3 at github. Main goal is to improve simplicity and performance. JDBM3 is packed with new features and changes. Difference from JDBM2 is even bigger than between JDBM1 and JDBM2. But there is still policy 'no test left behind', so we should enjoy great stability similar to previous releases."
path = "blog/jdbm_3_is_coming"
date = 2011-10-23
[extra]
render_title = false
+++

JDBM 3 is coming
======

A few weeks ago I started work on [JDBM 3 at github](https://github.com/jankotek/jdbm3). Main goal is to improve simplicity and performance. JDBM3 is packed with new features and changes. Difference from JDBM2 is even bigger than between JDBM1 and JDBM2. But there is still policy 'no test left behind', so we should enjoy great stability similar to previous releases.

<!-- more --> 

I already started work and some features bellow are actually already implemented (serialization, lazy tree values...). I expect to have first alpha version in January 2012 (all features implemented with usable stability). Jar file should remain very small, around 200KB.

Serialization
----
Most significant change is object serialization. JDBM2 used very primitive space efficient serialization for a few base classes (Long, Integer, ArrayList…). For rest of classes it uses java serialization.  Serialized data usually contains two section: class metadata (class and fields name and types...) and serialized data. Java serialization stores class metadata with each record and this creates huge space overhead.
More efficient is to store class metadata on single space and just reference those from each record. In JDBM3 I am going to reimplement Java serialization to do exactly this. As result space usage will be dramatically reduced. New serialization will be completely transparent to user and behave exactly as normal java serialization (Serializable, Externalizable etc...). This may look as huge step, but most of it is already implemented in JDBM3 github repository.

Improved defragmentation
---
Current defragmentation does not rearrange records, it just reclaims unused space. New defrag will reorganize records so tree nodes will be located on the same pages. This should significantly improve tree read operations. 

Large value stored outside tree
---
Currently all values are stored inside tree nodes. Even for simple lookup this means loading all values in node. If values are  big (1~kb) it slows down tree operations. In JDBM3 values larger than 32 bytes will be serialized into separate record and only reference id will be stored as part of tree. 'PrimaryStoreMap' is no longer necessary and will be removed.

RecordManager builder
---
JDBM2 uses properties to provide settings for RecordManager. This is very verbose and does not work with IDE hints. So JDBM3 replaces properties with new RecordManagerBuilder class. An example:

	  RecordManager recman = new RecordManagerBuilder("file.db")
	     .enableWeakCache().readonly().build();


New collections
---
JDBM currently provides HashMap and TreeMap collections. JDBM3 will introduce HashSet, TreeSet and LinkedList. 

Weak cache
---
There are small improvements in cache. Weak reference cache is added (we already have Soft). I am thinking about adding hard reference cache, but I have no valid use case for it. 

Read only store
----
It will be possible to open RecordManager in readonly mode. In this mode all insert/update/delete methods will throw 'OperationNotSupportedException'. Readonly store will not be locked and will be openable by multiple JVM instances.

Alternative storages
----
JDBM3 will introduce alternatives to traditional file storage. In-memory storage will store all data in RAM (useful for testing or bulk imports). In-jar readonly storage will read all data from compressed jar file. So user can deploy database over webstart or java-applet. It will be easy to copy database from one store to other, so you may do bulk import in memory and package it directly into zip file.

RecordManager write overlay
----
Want to write into read-only storage (jar file)? For this case JDBM3 introduces Write Overlay RecordManager. In this mode original read-only RecordManager is wrapped with proxy, which stores all modifications in second storage. For user it behaves exactly as single writable record manager. I expect this to be very usefull for testing and deployment on desktop.

Two file storage
-----
There were a lot of complains about JDBM2 using 8 files for storage. I would love to put everything into single file, but it is not possible. 
JDBM3 will have storage in two files: physical records and logical records. Keeping logical records separated greatly improves defragmentation and performance. 

Maven 2
-----
JDBM3 will use Maven2 instead of Ant. I will also add JDBM3 into main maven repositories. 

Faster transactions
----
JDBM1 had interesting feature when transaction were grouped and written into record file at once. This greatly improved performance with write modifications. I removed this feature in JDBM2, as it also caused frequent 'OutOfMemoryExceptions' (transactions were stored in memory). In JDBM3 this feature will be reintroduced, but with fix for memory consumption. 

Backups
-----
JDBM will be able to backup database into zip file, while running.

Space usage statistics
-----
Currently it is hard to tell how much space each structure uses. So JDBM3 will be able to printout same basic statistics about store, those are: unused space in store; min max and avg record size in store and each tree; total space consumed by each tree; number of nodes in tree etc.. This feature will be also important for development and performance profiling.

Free record sorting
-----
On each insert JDBM needs to find free slot for new record. Currently 'brutal force' scan across all free slots is performed. In JDBM3 I would like to keep free records sorted by size.  This would improve performance on inserts and updates. 

Serializers stored in tree
-----
Currently serializers are not inside tree, but are supplied outside by user. Now I think it is mistake and makes JDBM harder to use. So in JDBM3 serializers will be stored as part of tree definition in JDBM stored

Data format strictness
----
One of goals is to bring JDBM closer to SQL in terms of format definition and data consistency.
In JDBM2 there is no difference between creating new tree and loading existing. Now I think it is mistake, and JDBM should have more strict definition of data structures. So there will be separated method for creating new tree and loading existing trees. Secondary trees will also have more strict definitions. I will also add something similar to constraints from SQL. 

Single package
----
JDBM is now contained in single package 'jdbm'. Subpackages (recman, helper, btree and htree) were merged into single folder. Some classes were renamed to fit better into new structure (eg btree prefix). Internal classes (pages, free disk manager) should not be visible to user and are now package protected. Also I feel that JDBM has a few classes (~50) and there is no need for subpackages.

BTree and HTree completely replaced by maps
-----
There were two ways to manipulate trees in JDBM2. Now BTree or HTree classes can not be used directly, Map wrapper must be used instead. This makes API simpler and reduces code size. HTree now implements Map interface directly. BTree is package protected and still uses TreeMap wrapper.


Future
-----
JDBM 3 is last major version for years to come. I have no desire nor resources to move JDBM into clouds of clustering and super concurrency. JDBM will remain simple and fast storage for desktop and Android. In future I will concentrate on tooling and small improvements. For example I would love to have Spring support or GUI application to analyze record store. Also .Net port would be great.
