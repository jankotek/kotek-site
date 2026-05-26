+++
title = "More realistic view on Groovy"
template = "page.html"
description = "Realistic evaluation of Groovy based on half year usage in hobby projects."
path = "blog/more_realistic_view_on_groovy"
date = 2009-06-09
[extra]
render_title = false
+++

 More realistic view on Groovy
===
Realistic evaluation of Groovy based on half year usage in hobby projects.

<!-- more -->

OpenCoeli is my opensource pet project. Code size is around 200KB, 
it uses Spring, OpenJPA and Swing.  I decided to try Groovy 7 months 
ago after getting frustrated with Netbeans RCP, Maven2 and other bloated java 
frameworks. Main reason was good integration with java and builders for Swing. 
I was also flustrated with 'Java bloated framework ideology' and language
with 'Perl philosophy' looked as other extreme to try.

Adoption path
-----
Groovy evangelists presents it as 'drop-in java replacement' and they dont lie. 
Groovy have very  simular syntax and you can just rename *.java to *.groovy, correct a few common 
differencies and go. It also have joint-compilation to mix java and 
groovy code in same package.

I first started using Groovy as scripting language for Ant. 
After a while I started using it for unit tests. Groovy assertions also outputs 
expression values and reason why it failed so it did 
great job in there.

After two months I started using Groovy in main sources. It was not big switch, 
I simply used groovy for newly created classes.  

Compiler
----
Code mixing works great, you can declare class in groovy, extend it
in java, extends it again in groovy etc... But this complicates compilation little bit.
OpenCoeli with 200KB code takes 1 minute to compile from scratch and compiler 
requires 256MB of memory. With normal javac simular code is compiled under 5 seconds.
Luckily groovyc supports incremental compilation, so it is usable for daily development.

Other problem with Groovy 1.6 betas was Ant integration. Documented way did not worked and 
throw some NullPointer exceptions from Groovy internals. I did not check with new stable version,
but it is propably fixed. Groovyc also requires lot of memory and needs to be forked (not fixed yet).

This is code which worked for me:

    <!--define custom tasks -->
    <taskdef name="groovy" classname="org.codehaus.groovy.ant.Groovy" classpathref="classpath"/>
    <taskdef name="groovyc" classname="org.codehaus.groovy.ant.Groovyc" classpathref="classpath"/>

    <!-- compile production classes -->
    <target name="compile" description="compile the source">
        <mkdir dir="${bin}"/>

        <!-- compile groovy and java stuff -->
        <groovyc srcdir="src" destdir="${bin}" memoryMaximumSize="256m" failonerror="true" fork="true" >
            <classpath refid="classpath"/>
            <javac source="1.6" target="1.6" debug="on"/>
        </groovyc>
        <copy todir="${bin}">
            <fileset dir="src" includes="**/*"/>
        </copy>
    </target>


Compiler is stable, but have troubles in a few corner cases.  
Sometimes runs out of memory and some error messages are not very clear.
Most of my problems were because of 1.6 beta status, but even now (may 2009) groovyc 
have problems in some corner cases with number autoboxing and generics inheritance.  
But Groovy developers are working on this very seriously. When I reported problem with
compilation, I got reply with workaround in 16 hours.   

IDE
---
I had to switch IDE during this transition. Eclipse plugin was joke, 
Netbeans plugin was unstable and did not support Java joint compilation (Nov 2008). 
So I choosed IntelliJ Idea, it have very good Groovy helpers and have 
joint compilation (JetBrains actually wrote and donated joint compiler). 
JetBrains kindly donated licence for my opensource project. 

I started using Idea at version 8.0. 
This version had very slow compiler, and terrible bug so unit test were uncompilable.
I solved most of my problems by using Groovy plugin from lattest dev snapshot. 
With version 8.1.1 I can say I am finally happy, speed is good and bugs are fixed.

Refactoring for Groovy is very good. I would say simular to Eclipse 3.2. 
Refactoring have zilions  of options (rename, introduce method...)
and mostly are working correctly. Groovy is dynamic language so there are a few 
limitations, but Idea recognize them and ask for solution.

Code assistant for Groovy is also very good. Auto import, bug fixing, code 
completion etc works fine. Idea is integrated with InspectorGroovy so it 
can display lot of code warnings. For example if missing variable is used,
Groovy compiler will not catch it as error (dynamic language) but it is shown
as warning in editor. 

Code warnings have one problem with method parameters. If you have more methods
with the same name but different parameters, Idea does not know which method pickup
and show it as warning. For example this code shows warning:

	 OutputStream method definitions:
  		void write(int b)
		void write(byte b[])
		write(byte b[], int off, int len)
	 groovy code:
		byte[] b = ...;
		out.write(b);     


Code navigation works smoothly on mixed Java/Groovy code. Usage searching,
Hierarchy view, Structure view, jump to parent class etc.. everything is working
great. Idea have basic support for refactoring from Java to Groovy 
(dynamize inner classes). Support from Groovy back to Java is missing completely.
Usefull feature is Rename to Java/Groovy on file menu. 

Sometimes more advanced Idea features are not working with Groovy. For example
Idea recognizes JPA queries in Java code and offers JPQL code assistant on java 
strings. This does not work with Groovy.

Debuging Groovy code is little bit harder. Groovy have more complicated 
stack trace and simple 'Step into' brings you into Groovy runtime classes.
Solution is easy: add org.codehaus.groovy.* and groovy.* into Debug/Stepping black list, 
but is not set by default. Other very usefull feature would be stack trace filtering
on Output.  

So in short: Idea have very good IDE support for Groovy and in lattest version bug 
free. 

Performance
----
I found Groovy 1.1x to 2x slower then Java. Rumors about Groovy being 1000x slower 
are not true with Groovy 1.6. Also some memory overhead is here, but is small and 
I newer noticed it.

Root problem of Groovy performance is slow reflection API 
(java.lang.reflect.Method#invoke). JRE argument '-server' helps and 
realy boost Groovy performance (even on desktop app).

Groovy performance related problems are discoverable in profiler
(enable org.codehaus.groovy). In my app I found tree hotspots (sorting like tasks), 
refactoring those parts to Java code fixed problem.  

Strong typing and compilation
----
Groovy  have 'optional strong typing' and complier.
It is true, but there is one major differenct from Java:


	  //this code compiles, but fails during execution
  	  String s = "";
	  s.nonExistingMethod();


Groovy is dynamic language, so String#nonExistingMethod() can be added during 
runtime. In real it means that compilation does not guarantee much. 
This case is catched in editor code highlight, and Idea underscore it as problem 
'untyped member access'. But there is no way to make it fatal compilation error.
