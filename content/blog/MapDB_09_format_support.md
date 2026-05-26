+++
title = "MapDB 0.9 format support"
template = "page.html"
description = "MapDB has currently semi-stable branch 0.9.x. My plan was to keep stable API and storage format. However to support some new features (store size limit, async API) I have to make changes in storage format, which are not backward compatible. Also now I work full-time and project is evolving much faster than I expected."
path = "blog/MapDB_09_format_support"
date = 2013-07-01
[extra]
render_title = false
+++

MapDB 0.9 format support
========================

MapDB has currently semi-stable branch 0.9.x. My plan was to keep stable API and storage format. However to support some new features (store size limit, async API) I have to make changes in storage format, which are not backward compatible. Also now I work full-time and project is evolving much faster than I expected.

<!-- more -->

So I am going to make a few changes in the way MapDB is developed:

First there is not going to be storage backward compatibility between `0.9.N` releases. On every release you will have to completely re-import your data. 

Secondly API should be stable, but not set in stone. I have to support new stuff such as async operations. Some methods may get renamed or deprecated. This will be documented in release notes. Also `@Deprecated` annotations will be involved. The spirit of API (DBMaker, maps) is not going to change.

And thirdly releases will be much more often, probably weekly or biweekly. I just finished some major design tasks and prototyping. Now I can finally start fixing bugs and adding features.

There is also new release plan: 0.9 branch will be morphing until September. Then API and storage format will get frozen. Eventually 0.9 branch will mature and be renamed into MapDB 1.0 around December. 

This change will allow me to deliver stable MapDB 1.0 much earlier.
