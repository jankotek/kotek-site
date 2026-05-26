+++
title = "Using Ant and Javac without installation"
template = "page.html"
description = "Installing Ant and JDK can be pain. This post shows howto make Ant Java compiler part of your project. So it does not require installation. Only one external dependency needed to make build will be JRE. This setup makes it also much easier for new comers to start on project"
path = "blog/using_ant_and_javac_without_installation"
date = 2009-11-30
[extra]
render_title = false
+++

Using Ant and Javac without installation
======
Installing Ant and JDK can be pain. This post shows howto make Ant Java compiler part of your project. So it does not require installation. Only one external dependency needed to make build will be JRE. This setup makes it also much easier for new comers to start on project

<!-- more -->

Trick is to place Ant jars into your classpath and use manual script files to call them. Javac from JDK have many dependencies, but it can be replaced with compiler from Eclipse.

Step 1
------
Download Ant and place its jar files into **tools** subdirectory. For most purposes you will need those files: **ant.jar**, **ant-launcher.jar**, **ant-testutil.jar** and **ant-trax.jar**

Step 2
----
Create custom script to launch Ant. Create **ant.bat** file in root of your project. This will launch ant and forward all parameters to it. This launcher also adds all jars in **tools** and **lib** directory into classpath.


	java -Djava.ext.dirs=tools;lib -Xmx256m -jar tools/ant-launcher.jar  %1 %2 %3 %4 %5 %6 %7 %8 %9

And for Linux use **ant.sh**

	#!/bin/sh
	java -Djava.ext.dirs=tools;lib  -Xmx256m  -jar tools/ant-launcher.jar  $@


Also set file executable flat

	chmod 0755 ant.sh
	svn propset svn:executable ON ant.sh


Step 3
-----
Get Eclipse JDT Compiler. It is only 1.6 MB jar without any dependencies. Download it at [Eclipse Project Downloads](http://download.eclipse.org/eclipse/downloads/drops/R-3.5.1-200909170800/index.php) (search for JDT Core Batch Compile or 	ecj-3.5.1.jar). Then place this jar into **tools** directory

Step 4
----
Use Eclipse JDT Compiler. To make use out of new compiler you need to set one property in **build.xml**: 

	<!--
 	Use embedded Eclipse JDT javac. So JDK dont have to be installed.
	 This may cause problems on some IDEs. Comment it out then.
	-->
	<property name="build.compiler" value="org.eclipse.jdt.core.JDTCompilerAdapter"/>

Ant will use Eclipse JDT Compiler, so it will not require JDK. It will still display message 'tools.jar not found' but will compile just fine. 

NOTE
---
In some IDEs you may have problem because ECJ will not be in Ant classpath. Easiest workaround is to unset this property and install JDT. Other solution is to extend Ant path in your IDE to include ECJ.
