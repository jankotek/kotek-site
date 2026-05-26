+++
title = "scala problems"
template = "page.html"
description = "I love Scala, it lifted my capabilities and made me incredible productive. But after 18 months I found a few problems."
path = "blog/scala_problems"
date = 2011-07-06
[extra]
render_title = false
+++

scala problems
=========
I love Scala, it lifted my capabilities and made me incredible productive. But after 18 months I found a few problems.

<!-- more -->  

Compilation speed
---
Scala compilation is just bloody slow. My 'small' project with 200+ classes takes about 2 minutes to compile on quad core system.  It is about 10x slower than similar code in Java. Scala compiler does lot of additional stuff (type inference, implicit conversions), so it kind of makes sense. 

Incremental compilation just does not work yet
---
Eclipse (or any decent IDE) compiles Java as you type and reports errors almost instantly. Scala IDEs have incremental compilation as well, but it is still far behind Java. 

Incremental compiler in Idea is just slow, for example simple test case can take up to 20 seconds to recompile. It is also unreliable, often it reports missing classes and you need to fully rebuild project to fix it.

Eclipse incremental compiler is more interactive and more reliable then in Idea. But Scala Eclipse plugin is currently just better Notepad hooked to compiler, I would not call it IDE yet.

There are some workarounds, but best is change in  coding style; just dont run unit tests every 5 minutes as monkey.

Huge jars to distribute
---
Scala does lot of tricks to be fit into Java bytecode. For example each closure generated new *.class file. 

As result size of jar files grows rapidly. You also need to bundle Scala Library with program. Scala Library source code zip has 1.1 MB, compiled to Jar file it takes 8.5 MB. Size is problem when distributing desktop and mobile applications.

Workaround is easy, just use Pro-guard.

Not possible to return to Java
---
Scala is often presented as replacement to Java, but in real it brings programming to a new level. Scala extends mind and abilities. And after while it is just not possible to return back to Java.

To ilustrate: Scala has XML support. Not much just native XML literals support and XPath wired into language. And now after 18 months I just forgot how XML parsing is done in Java. 

Binary incompability
---
Scala changes class file format nearly every version. 2.7, 2.8 and 2.9 are not compatible with each other. But it gets even worse: 2.8.1 compiler can not compile with 2.8.0 library because it depends on some now classes. With a lot of Scala libraries, upgrade can become very painfull. 

Bugs and release cycle
---
Scala is just not as realiable as Java. There are bugs in compiler and libraries.  I usually discover new bug every 4 months. 

Look at recent version numbers: 2.8.0 then  2.8.1 then 2.9.0 and 2.9.0.1. There is not clear release cycle. 'Bug fix' releases may have new functionality and bugs. Scala 2.8.1 actually introduced worst bug I found, I spend 2 days hunting it down. 

And when new major version rolls out (2.8 or 2.9), you may forget about old version updates. It sucks when compared to PHP, Groovy or Python...

No tight loops
---

Scala is just not very good for tight loops.  Take this code:

	for(i <- 0 until 100){}

It translates to:

  * first new object is created: Range(1,100)
  * new Integer instance is created in each iteration
  * bunch of methods is called, creating overhead on method stack.

All this creates huge overhead, which makes loop many times slower. To get the same speed as with Java one have to use this construct:

	var i = 0
	while(i<100){
	 i += 1
	}



It is not about actors
---

Scala is somehow strongly associated with Actors. But it is just tiny tiny speck in Scala world. Scala let me write better Swing code, integrate tightly with JDBC, do much better XML processing, program Android... 

Yet some people have fetish about Actors. BTW I actually programmed on large application which uses Actor model. It is real pain in ars.
