+++
title = "Writing fast NIO webserver"
template = "page.html"
description = "I wrote fast and simple web server using New I/O and Kilim microthreads. No locks, no blocking, no channel selector. With a few optimization tricks, it is probably fastest webserver written in Java."
path = "blog/writing_fast_nio_webserver"
date = 2008-09-05
[extra]
render_title = false
+++

Writing fast NIO webserver 
======
I wrote fast and simple [web server](/down/asynchttpd-m2.zip) using New I/O and Kilim microthreads. No locks, no blocking, no channel selector. With a few optimization tricks, it is probably fastest webserver written in Java.

<!-- more --> 

Channel selector problems
-----
NIO is using [channel selector](http://java.sun.com/j2se/1.4.2/docs/api/java/nio/channels/Selector.html) as mechanism to dispatch events. It is promoted by Sun, and nearly all NIO based programs are using it. Good tutorial is [here](http://rox-xmlrpc.sourceforge.net/niotut/). 

Well known problems:

* Thread safety. Selector can be modified only from one thread. Also selecting channels should be single-threaded. 
* Some operations have undefined blocking. So your selection thread can be blocked and it is perfectly correct.
* Internally it uses HashSet as queue. It preserves items in random order, FIFO would be much better.

Less known problem is that selector simply dies under heavy load. 
Consider this example: fetching 3 KB file for 5 seconds. Webserver is Grizzly which internally uses selector. Total score is 12622 fetches/5 seconds ie **2524.39 fetches/sec**

	jan@artemis:~$ http_load  -parallel 200 -second 5 urlg.txt 
	12622 fetches, 166 max parallel, 4.5111e+07 bytes, in 5.00003 seconds
	3574 mean bytes/connection
	2524.39 fetches/sec, 9.02215e+06 bytes/sec
	msecs/connect: 0.862625 mean, 146.231 max, 0.043 min
	msecs/first-response: 4.82321 mean, 306.221 max, 2.067 min
	HTTP response codes:
	  code 200 -- 12622


And now same but longer 50 seconds. 


	28233 fetches, 179 max parallel, 1.00905e+08 bytes, in 50.0007 seconds
	3574 mean bytes/connection
	564.652 fetches/sec, 2.01807e+06 bytes/sec
	msecs/connect: 9.74712 mean, 3228.84 max, 0.04 min
	msecs/first-response: 5.32603 mean, 3000.25 max, 2.137 min
	HTTP response codes:
	  code 200 -- 28233


Resulting score is **564.652 fetches/sec**. Webserver simply gave up and start serving connections much slower after a few seconds under heavy load. 

I made some testing and I am nearly sure this problem is caused by Selector. 

And last problem with Selector? It is hard to use. There are some NIO libraries, which should help, but it still too complicated. 

Kilim microthreads
----
Classical approach is to have one thread for one connection. It makes programming much easy and simple. But threads are very resource hungry. Running thousands of threads in the same time is nearly impossible. 

But there is other solution: [Kilim microthreads](http://www.malhar.net/sriram/kilim/). Very lightweight threads which  inspired by Erlang. It is not problem to run milions microthreads in the same time. It uses some bytecode manipulation and stack restoration. It is definitely not problem to have one microthread per connection.

Kilim microthreads are using cooperative multitasking. Unlike preemptive it is not automatic, you must switch manually from programming code. Maybe it is not so cool, but is much more faster and simpler. Also it is easier to analyse and predict latency. Cooperative multitasking is for example used inside Linux kernel. 

Channels without selector
-------
With one microthread for each connection it is quite easy to use NIO without selector. 

First we need to listen and recieve new connection:


	// Kilim microthread is actually called 'Task'
	class ListenTask extends Task {

	// @pausable is for bytecode manipulations, 
	// execute method is like run() on java thread
	@pausable public void execute() {

	  //open port 8080
	  ServerSocketChannel ssc = ServerSocketChannel.open();
	  ssc.socket().bind(new InetSocketAddress(8080));      
	  //configure it as non blocking, VERY IMPORTANT!
	  ssc.configureBlocking(false);
	  //now listen for new connection in infinitive cycle
	  while (true){
	    //try to get new connection, accept() can also return null 
	    sc = ssc.accept();  
	    if(sc == null){
	      yield(); //no new connetion, switch to next microthread and wait a little
	      contiue;
	    }
	    sc.configureBlocking(false);
	    // create new task (microthread) which handle it
	    SessionTask ct = new SessionTask(sc);
	    //and start it
	    ct.start();
	  }  
	}
	}


If is needed to send some data in non blocking way:

	ByteBuffer buf = //data to send
	//perform cycle until all data has been send
	while(buf.remaining()!=0)
	{
	  int wr = sc.write(buf);
	  if(wr==0) 
	    //no data send this time, 
	    //give chance to other threads
	    yield();
}


In the same way you can recivie data. Parsing headers and other stuff is not here, you can check it directly [directly](/down/asynchttpd-m2.zip). 


Final tunning
-----
I found two problems:
  
* connection closing using Chanell.close() is blocking. It is needed to use reflection to call protected method which closes connection in non blocking way. It is not clearest solution, but everything for performance...
* You have to make dam sure that everything is send in one packet. Avoid packet fragmentation at any cost !

Current status
----
Webserver is in aplha stage, core is relatively stable. It can serve files, more extensions will came. More  [here](/down/asynchttpd-m2.zip).
