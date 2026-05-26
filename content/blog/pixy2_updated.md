+++
title = "Pixy2 updated"
template = "page.html"
description = "Pixy 2 System is an astronomical image examination and object identification application. It process raw images and makes basic corrections. It can also identify asteroids, comets and find variable stars. It was developed by Seiichi Yoshida, I took liberty and updated it a bit."
path = "blog/pixy2_updated"
date = 2011-11-01
[extra]
render_title = false
+++

Pixy2 updated
======

Pixy 2 System is an astronomical image examination and object identification application. It process raw images and makes basic corrections. It can also identify  asteroids, comets and find variable stars. It was developed by Seiichi Yoshida, I took liberty and updated it a bit.

<!-- more -->

[Original version](http://www.aerith.net/misao/pixy/index.html) was last updated in 2007, more than four years ago. Features of this program are impressive so I tryed to run it. But it depended on some outdated packages from ancient version of Java Runtime. 

I gave it a few hours and updated Pixy2 sources so it runs on recent JVM (1.6+). I also moved project source codes to Github, so now anyone can easily contribute new features.

So what I did:

  * I removed dependency on external XML parser. It is already bundled with recent JRE, so there is no need for external library
  * There was an external dependency on image library. I refactored it to use image library bundled with JRE
  * I dropped support for FITs (image library bundled with JRE is not that powerful).
  * A bit of refactoring to remove class name and keywords conflits
  * Fixed bunch of compilation warnings

Pixy2 is now polished and shiny, but it could still use some improvements. My plan is to add support for UCAC3 catalog and some online catalogs. And in some time I would like to make Pixy2 part of planetarium.

You can find updated version in [repository](https://github.com/jankotek/Pixy2), or you can [binary package](https://github.com/downloads/jankotek/Pixy2/pixy2.zip)
