+++
title = "Asterope"
template = "page.html"
[extra]
render_title = false
+++

Asterope
========
Asterope is an effort to develop an open-source feature-rich application for amateur astronomers. When finished it will provide sky charts, observation planning, telescope control, basic image processing and ephemeris. 

Asterope is developed as a companion to 16” inch telescope. By complexity it is somewhere between popular educational toys (Stellarium, WW Telescope) and professional tools (Aladin, Topcat).  It is right choice if you need finder chart for 13th magnitude planetary nebula, or recent
position of a not-yet-named asteroid.

It is work in progress. Major stable release is expected around 2016. First milestone is *Galway Sky Atlas*, large freely-printable 500 sky charts. It should prove that computer generated sky atlas can be as good as hand-optimized atlas. 

You may follow Asterope and get current source code at [Github](http://github.com/jankotek/asterope).

![M45](m45.jpg)


Why
------
There are already dozens of astronomical apps so why building just another? For two reasons:

First none of the existing applications provides stuff I would like to have. For example:  high quality printable finder charts, double star orbit visualizations or voice controlled telescope. Computers enable great things, but astronomical software seems to be stacked in 1990ties 

Second reason is community. There is no project anyone could just fork on Github and hack interesting feature over single evening.  Asterope is easy for new comers to pick-up. It is written in simple language (Java & Kotlin) with great IDE support. It also comes with unit tests, readable code, and good documentation. 

Other apps
-------------------------
There are many other open-source astronomical applications and Asterope ‘borrows’ from them heavily. But this project also gives back:
Our goal is to ‘cannibalize’ various small apps and libraries into single integrated package. It is done by refactoring, adding unit tests and sometimes complete rewrite. 

Current targets for ‘assimilation’ are:

* [Skyview](http://skyview.gsfc.nasa.gov/) is image mosaic stitching library. In Asterope it will provide spherical projections (WCS) and image morphing features. 

* [JParsec](http://conga.oan.es/~alonso/doku.php?id=jparsec) and [Solar System Simulator](http://conga.oan.es/~alonso/doku.php?id=projects). It provides ephemeris and realistic views for solar system objects. 

* [Orekit]( https://www.orekit.org/) provides tools for calculating orbital ephemeris. It will be used as library to predict satellite and asteroids positions. It should be also used to calculate binary star orbits. 

* [JSatTrack](http://www.gano.name/shawn/JSatTrak/)  predicts and visualizes satellites positions. We would like to implement this feature in Asterope.

* [Pixy2](http://www.aerith.net/misao/pixy/index.html) is image examination and object identification toolkit. After rewrite it will provide basic photometry, astrometry and image processing features. 

* [Alladin](http://aladin.u-strasbg.fr/) provides back-ground survey images (such as DSS or SDSS).  This feature is going to be integrated into Asterope. 

* [Virtual Moon Atlas](http://ap-i.net/avl/en/start) provides nice maps of the Moon. Asterope will reimplement its functionality, so it will be possible to use its maps and data files without conversion. 

* [Astroplanner](http://www.astroplanner.net/index.html) is an observation planning tool. It is not open-source. We would like to implement something very similar, but free. 

Some code developed for Asterope was already released in separate projects:

* JDBM4 is probably the fastest pure Java embedded database.

* Range Set extension to Healpix caused small revolution in astronomical spatial indexing.
