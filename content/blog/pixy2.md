+++
title = "Pixy2"
template = "page.html"
description = "I am not sure if you know Pixy2. It is very good program for making photometry on CCD image. It can also identify starts on CCD image. But Pixy2 depends on external XML parser and does not start with JRE 1.6 (internal XML parser)."
path = "blog/pixy2"
date = 2009-02-05
[extra]
render_title = false
+++

Pixy2
======
I am not sure if you know [Pixy2](http://www.aerith.net/misao/pixy/index.html). It is very good program for making photometry on CCD image. It can also identify starts on CCD image. But Pixy2 depends on external XML parser and does not start with JRE 1.6 (internal XML parser).

<!-- more -->

I modified source code to compile under Java 1.6 and recompile it. Now it is possible to run this software on JRE 1.6. Release jar is [here](https://github.com/downloads/jankotek/asterope/pixy2-20090205.zip). 

To run it just install JRE 1.6 and double click on Pixy2. 

In near future I have plans to merge catalogs readers into OpenCoeli. In longer terms I want fully integrate photometry and identification algorithms with OpenCoeli canvas, datasources and scripting 


UPDATE on 1.11.2011
----
Pixy2 is now located on Github. Find out more in new [blog post](/blog/pixy2_updated/)
