+++
title = "SwingUtilities.invokeAndWait with return value"
template = "page.html"
description = "Threading in Swing is tricky. In many cases it is necessary to make a calculation on EDT thread and receive result back. For example components should not be created outside of EDT, or values should be accessed in thread safe way."
path = "blog/swingutilities.invokeandwait_with_return_value"
date = 2010-11-11
[extra]
render_title = false
+++

SwingUtilities.invokeAndWait with return value
======
Threading in Swing is tricky. 
In many cases it is necessary to make a calculation on EDT thread and receive result back. For example components should not be created outside of EDT, or values should be accessed in thread safe way.

<!-- more --> 

Method invokeAndWait could be used for calculation, but it does not have return value. Also Runnable interface passed as argument is not very usefull.  Solution is to update invokeAndWait to accept Callable interface. 

From Callable javadoc:

	The Callable interface is similar to Runnable, in that both are designed 
	for classes whose instances are potentially executed by another thread.  
	A Runnable, however, does not return a result and cannot throw 
	a checked exception.


So there are  two problems: First value needs to be transfered between two threads. 
Second, if Callable fails with exception, it should be thrown in original thread. 
And here is solution:


	public static <E> E invokeAndWait(final Callable<E> r){ 
		final AtomicReference<E> ref = new AtomicReference<E>(); 
		final AtomicReference<Exception> except = new AtomicReference<Exception>();
		onEDTWait(new Runnable(){
			public void run() {
				try {
					ref.set(r.call());
				} catch (Exception e) {
					//pass exception to original thread
					except.set(e);
				}				
			}});
		if(except.get()!=null)
			//there was an exception in EDT thread, rethrow it
			throw new RuntimeException(except.get());
		else
			return ref.get();
	}

Methods accepts Callable as argument. This callable is executed on EDT thread, using original invokeAndWait. AtomicReference is used to pass result value back to original thread. 
If Callable throws an exception, it is passed back to original thread. 
All this is nicely wrapped with generics, so there is no casting necessary. Usage is deadly simple,
this example creates new instance of JPanel in thread safe way. 


	//executed outside of EDT
	JPanel panel = invokeAndWait(new Callable<JPanel>(){
	public JPanel call() throws Exception {
		//executed inside EDT
		return new JPanel();
	}});
	//continue outside of EDT	


or you can access value of existing instance in thread safe way:

	//executed outside of EDT
	Integer width = invokeAndWait(new Callable<Integer>(){
	public Integer call() throws Exception {
		//executed inside EDT
		return panel.getWidth();
	}});
	//continue outside of EDT	

**note:** getText(), setText() and some other methods are thread safe. So it is safe to access them outside of EDT. Always check javadoc! 


Scala
---
All those wrapper classes does not help readability. So here is similar implementation in Scala with closures:

	/** wraps closure into runnable*/	
	final def Runnable(block: =>Unit) = new Runnable {
		def run = block
	}

	final def invokeAndWait[E](block: => E):E = { 
	  var ret:Option[E] = None;
	  SwingUtilities invokeAndWait Runnable({ret = Some(block)})	  
	  return ret.get		   
	}


It works similar way as Java example, but uses closure instead of Callable. Usage is deadly simple:

 	val panel = invokeAndWait{ new JPanel()}
	val width = invokeAndWait{panel.getWidth()}
