+++
title = "JDBM4 renamed to MapDB"
template = "page.html"
description = "'JDBM' (Java Database Manager) name has long history. Original 'DBM' (Database Manager) has been introduced in seventies. Java version started in 2001 and first stable version was introduced in 2005. Until 2012 it has dozen forks including JDBM2,3,4 and ApacheDS."
path = "blog/JDBM4_renamed_to_MapDB"
date = 2012-11-03
[extra]
render_title = false
+++

JDBM4 renamed to MapDB
=====================

'JDBM' (Java Database Manager) name has long history. Original 'DBM' (Database Manager) has been introduced in seventies. Java version started in 2001 and first stable version was introduced in 2005. Until 2012 it has dozen forks including JDBM2,3,4 and ApacheDS.

<!-- more --> 

So what are search results for 'JDBM'? 

Until recently Google was suggesting correction 'JDBC' instead of 'JDBM'. [Current results](https://www.google.com/search?hl=en&tbo=d&output=search&sclient=psy-ab&q=jdbm&btnK=)
has JDBM1 on first position (10 years old SourceForge page). On second position is obsolete JDBM2 on GoogleCode. Then comes lot of junk and finally JDBM3 on third page and JDBM4 somewhere on 15th page. 

[Maven Central](http://search.maven.org/#search%7Cga%7C1%7Cjdbm) repository returns about 15 projects. Absolutely worst is [situation on Twitter](http://twitter.com/search?q=jdbm&src=typd). First I thought that JDBM has lot of teenage fans. But there is singer named 'Justin Drew Bieber Mallete' and he seems to be more popular than my little database. 

Until JDBM was just my toy project search results were not that important. But JDBM4 is different beast, it _is_ the fastest Java database and  it will have millions of users. In future I may even start company around this software project. So it needs strong and unique brand.

MapDB
-----
Most important feature on JDBM is that it directly implements `java.util.Map` interfaces. So I choosed 'MapDB' name (second candidate was 'DiskMap'). Suprisingly this name is almost completely free; there are no projects, trademarks or websites with such name. 

So now what?

 * JDBM4 package name will be renamed to `org.mapdb` (I already registered domain)

 * JDBM4 Github project will be renamed to `mapdb`. History, bugs and followers will be preserved. I will put redirect notice to original URL.
 
 * 'Official' project address will be 'www.mapdb.org', with redirect to Github page
 
 * Mail group `jdbm@googlegroups.com` will be renamed some time in the future. History and users will be preserved, email address will change.
