+++
title = "Spring bean name resolver"
template = "page.html"
description = "OpenCoeli is heavily using Spring IOC framework. It is great, but is missing one feature: inverse bean name resolver. Why it is good to know bean name? For example for configuration, if you inject different bean you just need to save bean name. Also it can be very useful for logging."
path = "blog/spring_bean_name_resolver"
date = 2007-08-21
[extra]
render_title = false
+++

Spring bean name resolver
=========================

OpenCoeli is heavily using Spring IOC framework. It is great, but is missing one feature: inverse bean name resolver. Why it is good to know bean name? For example for configuration, if you inject different bean you just need to save bean name. Also it can be very useful for logging.

<!-- more --> 

So here is my implementation of spring bean name resolver. It is using `BeanPostProcessor` to register bean names to map shortly after their creation. Map is  `WeakHashMap` so it does not prevent beans being GCed. 

The name resolver is method `public String getBeanName(Object bean)` where you pass an bean and it returns its name. If bean is not known, it returns null.

Here is code of class

	package org.opencoeli.context;

	import java.util.WeakHashMap;

	import org.springframework.beans.BeansException;
	import org.springframework.beans.factory.config.BeanPostProcessor;

	/**
	 * Object which resolves bean names.
	 * <p>
	 * It process newly create beans and save them with name to WeakHashMap.
	 * Because it is weak, it does not prevent garbage collection
	 * 
	 */
	public class SpringBeanNameResolver implements BeanPostProcessor{

    /**
     * !!!!!!! MUST BE WEAK !!!!!!!
     */
    private WeakHashMap<Object,String> beanNames = new WeakHashMap<Object,String>();
    
    
    /**
     * returns bean name if bean was created by Spring framework
     * 
     * @param bean
     * @return bean name
     */
     public String getBeanName(Object bean){
        return beanNames.get(bean);
    }
    
    
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {   
        return bean;
    }

    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        //put bean and its name to weak hash map
        beanNames.put(bean,beanName);
        return bean;
    }
	}


And of course you must register this class as bean in Spring XML files. 

	<code xml>
	<bean id="beanNameResolver" class="org.opencoeli.context.SpringBeanNameResolver"/>	
	</code>

This implementation is very simple, feel free to modify that. For example you can declare `map` and `getBeanName` as static. Also to prevent some multithreadind issues you can use synchronized map from `Collections` class. 

I am not 100% sure that this bean will catch all beans. Simply because their can be instantiated **before** this class. For example if other bean implements `BeanPostProcessor` too. For more details look at Spring documentation and source codes. 

Node: OpenCoeli is distributed under GPL2, but this sample is under BSD licence.
