+++
title = "Enumeration problem at Scala 2.8.1"
template = "page.html"
description = "Scala is great language and I love it. But sometimes one can found strange stuff in there. A few weeks ago I updated Scala library in my project from 2.8.0 to 2.8.1. There were a few minor issues. But also one really big one. It took me a few hours to find reason why my tests are failing."
path = "blog/enumeration_problem_at_scala_2.8.1"
date = 2010-12-20
[extra]
render_title = false
+++

Enumeration problem at Scala 2.8.1
======
Scala is great language and I love it. But sometimes one can found strange stuff in there. A few weeks ago I updated Scala library in my project from 2.8.0 to 2.8.1. There were a few minor issues. But also one really big one. It took me a few hours to find reason why my tests are failing.

<!-- more -->

And problem? Scala 2.8.1 introduced bug in Enumeration. Thanks to this bug Enumeration is not so immutable. Have look at this code:


        object WeekDay extends Enumeration {
          type WeekDay = Value
          val Mon, Tue, Wed, Thu, Fri, Sat, Sun = Value
        }

        WeekDay.values.foreach(s=>print(s+", "))
        // >> Mon, Tue, Wed, Thu, Fri, Sat, Sun,
        println("")
        WeekDay.values.foreach(s=>print(s+", "))
        // >> Mon, Tue, Wed, Thu, Fri, Sat, Sun, Value, 
        println("")
        println("Enum size: "+WeekDay.values.size)
        // >> Enum size: 8 
        //assertion fails
        assert(WeekDay.values.size == 7) 
       


Enumerations.values is returning an extra element. It does not happend on first call, but second and third. It is easy to imagine test case which would let this bug pass. However, 2.8.1 should be bug fix release, and such things should not simply happen.
