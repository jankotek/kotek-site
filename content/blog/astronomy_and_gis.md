+++
title = "Astronomy and GIS"
template = "page.html"
description = "There is entire engineering discipline called Geographic information system, it is all about how to draw maps and present various informations on Earth's surface. About GIS was written many books."
path = "blog/astronomy_and_gis"
date = 2007-07-30
[extra]
render_title = false
+++

Astronomy and GIS
=================
 
There is entire engineering discipline called [Geographic information system](http://en.wikipedia.org/wiki/Geographic_information_system), it is all about how to draw maps and present various informations on Earth's surface. About GIS was written many books.

<!-- more --> 

More importantly there are many programs in this area. In initial phase I was investigating if it is possible to 'bend' one of them for astronomical use. 

Geography and astronomy have many similar things:

* both are presenting data on sphere
* both deal with large volumes of data (milion houses X milion stars)
* both are using various coordinate system

Astronomy have few specific, basically their are well described in [this post](http://www.nabble.com/Astronomical-extensions-tf2510259.html).  (this list is citation)

* Astronomers deal with ellipses, and often care very much about ellipse-specific things 
* Astronomers use a totally different set of coordinate systems.
* Projections are different,  A very basic gnomonic projection is by far the most common, but it is described very differently (not to mention the fact that everything is inside-out, since we look at the sky, not the ground)

All of those problems are not hard to fix. Ellipse can be described as polygonal area, astronomical coordinate systems are not so unique and can be implemented in GIS  and projection is just one class.

In GIS there is many frameworks which would be pleasure to use. For example [GeoTools](http://geotools.codehaus.org/) looks vary promising. Library like this  can save loot of time. 

Also [spatial extensions for databases](http://dev.mysql.com/tech-resources/articles/4.1/gis-with-mysql.html) looks very promising. Their allow SQL queryes like 'where distance(a,b)<100km).  

So why is not OpenCoeli map library based on GIS? Where is the catch? And why it does not uses spatial extensions?

The catch is that in GIS it is possible not to use spheric geometry, but simple 2D Cartesian xy system. Biggest data sets used in GIS covers only few degrees of globe (For example database of houses in USA). But astronomy is dealing with datasets which covers entire sphere. Abstraction to 2D Cartesian system is not simply possible. We need full spherical 2D geometry. 

Other problems is character of data. GIS is dealing mostly with areas (land) and lines (roads). Astronomy have mostly points. GIS databases and data structures are focused in different way. 

Third problem is that GIS have big knowledge overhead. It is dealing with geoids, many rules and situations which are useless in astronomy. So finally I decide not to base map library on GIS. 

But code reusability must be. OpenCoeli is using some libraries from GIS. Most visible is [java projection library](http://www.jhlabs.com/java/maps/proj/), thanks to it OpenCoeli supports about 50 different projections. Also GIS map renderers are very useful source of info about Java2D.
