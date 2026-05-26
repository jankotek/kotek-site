+++
title = "Kotlin pre-pre-pre alpha survival guide"
template = "page.html"
description = "Jetbrains recently open-sourced Kotlin, so you may want to take it for a quick spin. Here are a few tips and workarounds. I worked with Kotlin last few weeks as volunteer tester, I am not connected with Jetbrains."
path = "blog/kotlin_pre-pre-pre_alpha_survival_guide"
date = 2012-02-16
[extra]
render_title = false
+++

Kotlin pre-pre-pre alpha survival guide
======
Jetbrains recently open-sourced Kotlin, so you may want to take it for a quick spin. Here are a few tips and workarounds. I worked with Kotlin last few weeks as volunteer tester, I am not connected with Jetbrains.

<!-- more -->

First keep on mind that this is very early version. It is usable for learning, but have lot of sharp edges and bugs. And Jetbrains are moving at light speed so it is probably worth to wait couple of months for more stable version.

Setting up 
----
You will need an early build of Idea 11.1, grab it [here](http://confluence.jetbrains.net/display/IDEADEV/IDEA+11.1+EAP). Then download plugin snapshot  from [github](https://github.com/JetBrains/Kotlin/downloads). From Settings/Plugins use 'Install plugin from disk...' button. Kotlin does not have special nature (as Scala), you will be able to create Kotlin 'kt' file directly on any Java project.

More about setting up in official [announcemenent](http://blog.jetbrains.com/kotlin/2012/02/kotlin-goes-open-source-2/)


What works, what does not
---
What works

  * nullability
  * inheritance
  * generics
  * collection methods (map, fold..)
  * extension methods
  * inference

What semi works

  * inference in combination with collection methods, sometimes need extra typing hint for help
  * unit tests (need workarouds)
  * compiler still often crashes on some less usual language construct (for example empty closure)

What does not work

  * Java cross compilation (IDE works, but compiler just fails)
  * public/private 
  * access getter/setter as fields

My overall impression is that Jetrains concentrated on a few critical parts and done those well, some other parts are in progress or missing. IDE is superb for this early stage. Typing system and nullability are working well. And overall it fails very predictable, and is easy to find problematic parts of code.


Source code to study
----
I assume you read [Confluence](http://confluence.jetbrains.net/display/Kotlin/Welcome) and played with [webdemo](http://kotlin-demo.jetbrains.com/). Next level is to study [stdlib unit tests](https://github.com/JetBrains/kotlin/tree/18c480ba98bc1154eee06530df310fc6361d3933/testlib/test), it captures current state of language. So you wont waste time with not-yet-implemented features.  

Collections
----
I was mostly experimenting with collections methods. Kotlin brings functional collections similar to Scala. It is implemented as a few extension methods on top of Java Collection Framework. So it is pretty lightweight. There is no immutability yet, preferred collection is array or ArrayList.
 Relevant unit tests is [here](https://github.com/JetBrains/kotlin/blob/18c480ba98bc1154eee06530df310fc6361d3933/testlib/test/CollectionTest.kt).

Type inference is not yet as good as in Scala, but this will improve. So it sometimes needs little hint. For example map, please note <String,Int>


	fun main(args : Array<String>) {
    		val o = array("aa","bb")
		//this fails
		//val o2 = o.map{it.length()}
		//this works
		val o2 = o.map<String,Int>{it.length()}

		println(o2);
	}


Also nullability can be a bitch:

	fun main(args : Array<String>) {
	    	val o = "aa,bb,cc".split(",").sure()
    		//this fails
		//val o2 = o.map<String,Int>{it.length()}
		//this works
		val o2 = o.map<String?,Int>{it.sure().length()}

		println(o2);

	}

I would always suggest to look at relevant test if you run into problem. And sometimes it is just easier to use for loop.

Fun with runnables
----

I tried to implement Runnable and Callable wrapper for closure. I started with class which implements interface and takes closure as constructor parameter. But I found yet another compiler error and started digging into test cases. Workable solution was this:


	fun runnable(val block:() -> Unit) = object: Runnable{
    		override fun run(){
		        block()
		}
	}

	fun callable<E>(private val block:()->E) = object: java.util.concurrent.Callable<E>{
	    override fun call():E = block()
	}



Unit tests
---

I use JUnit 3. Minimal test looks like this:


	import std.*
	import std.io.*
	import std.util.*

	import junit.framework.Assert.* //to get assert* methods
	import junit.framework.TestCase


	class ResourceMapTest() : TestCase(){

	 	fun testAA(){
        		assertEquals(1,1)
		}
	}


It is step down from Scala with its '===' operator. But I actually like it, it keeps tests simple and easy to debug.

Not sure if it is general error, but my Idea could not run unit tests. Classes were compiled into 'out/production' folder and test runner could not find them. Workaround is to use text runner:

	 junit.textui.TestRunner our.TestCase



Summary
----
After couple of evenings I ported small application from Scala to Kotlin. I spend about 50% time trying to workaround compiler bugs. I could easily reduce this time by using less advanced construct (for-loop instead of Collection.map).

Kotlin IDE is fantastic (given current state). Compiler works good in core areas. I would not yet recommend using Kotlin for pet-project at current state (unless you want to do testing). But for learning code snippets it is great.
