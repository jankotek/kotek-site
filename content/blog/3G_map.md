+++
title = "3 billion items in Java Map with 16 GB RAM"
template = "page.html"
description = "One rainy evening I meditated about memory managment in Java and how effectively Java collections utilise memory. I made simple experiment, how much entries can I insert into Java Map with 16 GB of RAM?"
path = "blog/3G_map"
date = 2012-11-12
[extra]
render_title = false
+++

3 billion items in Java Map with 16 GB RAM
========================================================

One rainy evening I meditated about memory managment in Java and 
how effectively Java collections  utilise memory. 
I made simple experiment, how much entries can I insert into 
Java Map with 16 GB of RAM?

<!-- more -->

Goal of this experiment is to investigate internal overhead of collections.
So I decided to use small keys and small values. All tests 
were made on Linux 64bit Kubuntu 12.04. JVM was 64bit Oracle Java `1.7.0_09-b05` with HotSpot `23.5-b02`. 
There is option to use compressed pointers (-XX:+UseCompressedOops), which is on by default on this JVM.

First is naive test with `java.util.TreeMap`. It inserts number into map, until it runs out of memory and ends with exception. 
JVM settings for this test was `-Xmx15G`

    import java.util.*; 
    Map m = new TreeMap();
    for(long counter=0;;counter++){
      m.put(counter,"");
      if(counter%1000000==0) System.out.println(""+counter);
    }
        
This example ended at 172 milion entries. Near the end insertion rate slowed down thanks to excesive GC activity. 
On second run I replaced `TreeMap` with `HashMap, it ended at 182 milions. 

Java default collections are not most memory efficient option. So lets try an memory-optimized . I choosed `LongHashMap` from MapDB, which uses primitive long keys and is optimized to have small memory footprint. JVM settings is again `-Xmx15G`
    
    import org.mapdb.*
    LongMap m = new LongHashMap();    
    for(long counter=0;;counter++){
      m.put(counter,"");
      if(counter%1000000==0) System.out.println(""+counter);
    }

This time counter stopped at 276 million entries. Again near the end insertion rate slowed down thanks to excesive GC activity.      
It looks like this is limit for heap-based collections, Garbage Collection simply brings overhead.

Now is time to pull out the big gun :-). We can always go *of-heap* where GC can not see our data. Let me introduce you to [MapDB](http://www.mapdb.org), it provides concurrent TreeMap and HashMap backed by database engine. It supports various storage modes, one of them is off-heap memory.  (disclaimer: I am MapDB author).

So lets run previous example, but now with off-heap Map. First are few lines to configure and open database, it opens direct-memory store with transactions disabled. Next line creates new Map within the db. 

    import org.mapdb.*

    DB db = DBMaker
       .newDirectMemoryDB()
       .transactionDisable()
       .make();

    Map m = db.getTreeMap("test");
    for(long counter=0;;counter++){
      m.put(counter,"");
      if(counter%1000000==0) System.out.println(""+counter);
    }

This is off-heap Map, so we need different JVM settings: `-XX:MaxDirectMemorySize=15G -Xmx128M`. This test runs out of memory at 980 million records.  

But MapDB can do better. Problem in previous sample is record fragmentation, b-tree node changes its size on each insert. Workaround is to hold b-tree nodes in cache for short moment before they are inserted. This reduces the record fragmentation to minimum. So lets change DB configuration:

    DB db = DBMaker
         .newDirectMemoryDB()
         .transactionDisable()
         .asyncFlushDelay(100)
         .make();
         
    Map m = db.getTreeMap("test");         

This records runs out of memory with *1 738 million records*. Speed is just amazing 1.7 bilion items are inserted within 31 minutes.
         
MapDB can do even better. Lets increase b-tree node size from 32 to 120 entries and enable transparent compression:

       DB db = DBMaker
                .newDirectMemoryDB()
                .transactionDisable()
                .asyncFlushDelay(100)
                .compressionEnable()
                .make();

       Map m = db.createTreeMap("test",120, false, null, null, null);

This example runs out of memory at whipping *3 315 million records*. It is slower thanks to compression, but it still finishes within a few hours. I could probably make some optimization (custom serializers etc) and push number of entries to  somewhere around 4 billions.
    
Maybe you wander how all those entries can fit there. Answer is delta-key compression. Also inserting incremental key (already ordered) into B-Tree is best-case scenario and MapDB is slightly optimized for it. Worst case scenario is inserting keys at random order:

_UPDATE added latter: there was bit confusion about compression. Delta-key compression is active by default on all examples. In this example I activated aditional zlib style compression._
    
        DB db = DBMaker
                .newDirectMemoryDB()
                .transactionDisable()
                .asyncFlushDelay(100)
                .make();

        Map m = db.getTreeMap("test");

        Random r = new Random();
        for(long counter=0;;counter++){
            m.put(r.nextLong(),"");
            if(counter%1000000==0) System.out.println(""+counter);
        }

But even with random order MapDB handles to store 651 million records, nearly 4 times more then heap-based collections. 
    
This little excersice does not have much purpose. It is just one of many I do to optimize MapDB. Perhaps most amazing is that insertion speed was actually wery good and MapDB can compete with memory based collections.
