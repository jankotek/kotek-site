+++
title = "Label layout algorithm"
template = "page.html"
description = "One of most common problems in astro cartography are labels. There is many objects on map and many of them have an label. In highly concentrated areas (galaxy clusters, Saggitarius) it is hard to place label without overlaping with other objects and labels."
path = "blog/label_layout_algorithm"
date = 2009-01-17
[extra]
render_title = false
+++

Label layout algorithm
======
One of most common problems in astro cartography are labels. There is many objects on map and many of them have an label. In highly concentrated areas (galaxy clusters, Saggitarius) it is hard to place label without overlaping with other objects and labels.

<!-- more --> 

Most programs are just ignoring this problem and let labels overlap. PP3 which is considered as most advanced astro cartography program, is using script where you can change position labels manualy.

I recently implement label auto positioning alghorithm for OpenCoeli. It calculates score for each label position and use best. Score is based on 'color distance from background'. In short it places labels on places where is nothing.

It is 'first prototype', but already working wery well. And there is still place for even better results and speed optimalizations.

Some screenshots:

![orion](/img/blog/labelori.png)

![m13](/img/blog/labelm13.png)
