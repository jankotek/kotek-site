+++
title = "RangeSet and huge datasets"
template = "page.html"
description = "Most of collections does not use memory efficiently. But there is simple compression trick to store virtually unlimited data sets. And there are practical implementations."
path = "blog/rangeset_and_huge_datasets"
date = 2009-11-30
[extra]
render_title = false
+++

RangeSet and huge datasets 
======

Most of collections does not use memory efficiently. But there is simple compression trick 
to store virtually unlimited data sets. And there are practical implementations.

<!-- more -->

First little bit of theory. Lets have Java SortedSet of Long numbers. It have a few basic features:

* Values in set are unique, there are  duplicates. 
* Contains() operation is indexed and fast.
* Values in set are sorted lowest to highest. 

This data structure can be implemented in various way. Most common is **TreeSet** which uses BTrees structure. 
More modern variant is **SkipList**. But all of those structures does not use memory very efficiently. 
Their memory consumption grows linearly with their size. 

To save same memory one can store values in **sorted long[] array** and 
use binary search to find values. This is consuming way less memory, because object are not created, and 
only primitive values are stored. Trade off is the same as with ArrayList, inserts require moving arrays 
around and are generally very slow.

Other way to save memory can be [BitSet](http://java.sun.com/j2se/1.4.2/docs/api/java/util/BitSet.html). 
But its usage is very limited. More smart structures are 
[Compressed BitSets](http://www.google.com/search?rls=en&q=compressed+bitset) but their usage
is even more limited. 

Ranges
----
In case data are grouping in continuous intervals compression is very simple. 
Only first and last values needs to be stored. So instead of bunch of number item in set will be:

	class Range{
		long first;
		long last;
	}

This brings some new problems. First it needs to handle range overlaps on inserts. Second is 
contains operation for single number. 

There are plenty of implementations. Most notable is [LongRangeSet](http://pcj.sourceforge.net/docs/api/bak/pcj/set/LongRangeSet.html)
from [Primitive Collections for Java](http://pcj.sourceforge.net/). This implementation uses 
Range object stored in sorted list. 

Completely without object overhead is this [RangeSet](http://www.google.com/codesearch/p?hl=en#KYLvKSOdAFc/trunk/contrib/fec/common/src/com/onionnetworks/util/RangeSet.java&q=com.onionnetworks.util.RangeSet&d=7)
It stores range boundaries in sorted long[] array. Range starts are at even positions, range ends are at odd position.
This organization is very effective in memory consumption and fast for read only operations. 
But inserts are taking longer.

And there is even implementation for [.Net](http://www.codeproject.com/KB/recipes/rangeset.aspx?msg=1101152)

Operations
----
Data compressed in memory are nice, but howto process them without doing decompression and running out of 
memory? Iteration is quite simple to imagine, but what about some others?

Most typical spatial operations are logical operations on items in set: union, intersection and complement.
Those operations produce other set. This operations can be implemented very efficiently. 

LongRangeSet
----
And here is my implementation of [LongRangeSet](http://healpix-rangeset.googlecode.com/svn/trunk/healpix-rangeset/src/org/asterope/healpix/LongRangeSet.java).
It is part of bigger project [Healpix-RangeSet](http://code.google.com/p/healpix-rangeset/). In this 
project it stores huge set of astronomical spatial data.

By replacing ArrayList by RangeSet performance of Healpix skyrocketed. Memory consumption decreased from 
gigabytes to megabytes. And area generation speed up from hours to seconds. 

LongRangeSet also implements union, intersection and complement very efficiently. Each operation uses
only one pass over ranges and new set is constructed on the fly.
