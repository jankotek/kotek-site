+++
title = "Spring and memento pattern"
template = "page.html"
description = "Memento pattern is common way howto save and restore object state. It is used in many applications including Eclipse and Netbeans. Implementation in OpenCoeli is easy to use, Spring friendly and very simple."
path = "blog/spring_and_memento_pattern"
date = 2007-09-17
[extra]
render_title = false
+++

Spring and memento pattern
======
[Memento pattern](http://en.wikipedia.org/wiki/Memento_pattern) is common way howto save and restore object state. It is used in many applications including Eclipse and Netbeans. Implementation in OpenCoeli is easy to use, Spring friendly and very simple.

<!-- more --> 

Object state is usually saved to somekind of properties, for example to [IMemento](http://help.eclipse.org/help31/topic/org.eclipse.platform.doc.isv/reference/api/org/eclipse/ui/IMemento.html) from Eclipse. Other approach is to save state to serializable object, it is called Externalization (external object). It have support in [JRE](http://java.sun.com/j2se/1.4.2/docs/api/java/io/Externalizable.html) and is also very common in Netbeans. 

Both ways how advantages. Properties can be transformed to text or XML file. Externalization is easier to use, becouse you do need to transform your configuration to different data format. For example storing `Map<String,String>` is very easy with serialization. OpenCoeli implementation have both advantages, external object is serialized to XML file.

It is possible thanks to magic library called [XStream](http://xstream.codehaus.org/), very simple and easy to use XML serialization/deseralization tool. It is real time saver and is also usefull for debuging or logging. 

So here is implementation in OpenCoeli. First interface of object which can save and restore its configuration:



	package org.opencoeli.context.config;

	/**
 	* Object which can persist its state to memento and restore itself
	 * from memento. 
	 * <p>
	 * Memento can be any serializable type. Map is recommended
	 *    
	 */
	public interface CoeliPersistable<E>{

    /**
     * save state to memento
     * 
     * @return memento, can be any serializable type
     */
    E saveState();
    
    /**
     * restore state from memento 
     */
    void restoreState(E memento);

    /**
     * return persistence under which will object be stored.
     * <p>
     * if return is null, then full class name will be used
     * 
     * @return ID under which result is persistent
     */
    String getPersistenceID();    
	}



In `saveState()` object creates memento and save its state to it. `restoreState(E memento)` is used to restore objects state shortly after initialization. PersistenceID is 'file name' under which configuration should be saved. 

And here practical example:



	package org.opencoeli.map;

	//...snip...

	public class PositionHelper implements CoeliPersistable<PositionHelperMemento>{

		//...snip...

    		public String getPersistenceID() {
		        return null;
		}

		public void restoreState(PositionHelperMemento memento) {
	        	//projection must be first !!!
	        	if(memento.projection!=null )
	        	    setProjection((CoeliProjection)CoeliContext.getBean(memento.projection));        
	                
	        	setViewAngle(memento.viewAngle);
	        	setCentralLocation(memento.centralRa,memento.centralDec);
		}

		public PositionHelperMemento saveState() {
	        	PositionHelperMemento m = new PositionHelperMemento();
	        	m.viewAngle = viewAngle;
	        	m.centralRa = centralRa;
	        	m.centralDec = centralDec;
	        	m.projection = CoeliContext.getBeanName(projection);
	        	return m;
	    	}
    
	}

	class PositionHelperMemento {
	    double viewAngle;
	    double centralRa;
	    double centralDec;
	    String projection;
	}



PositionHelper is helper class for counting position. As you can see it stores some numbers (position and zoom) and also Projection. 

This is interesting part: Projection is actualy Spring bean injected by Spring framework and changeble in configuration dialogs. User can inject other bean implementation from GUI on the fly. Changes are persistable, wiring in Spring XML files is just default value. Persisting entire bean is not reasonable, so only bean name is persisted

PositionHelperMemento is persistent object which holds configuration. It should not contain any logic (even getters and setters). It cannot be inner class, because inner classes stores invisible reference to outer class (try Outher.this) and are serialized with it. 

Of course you can use any serializable object directly (Map, List..). But I would recommend an protected object, in future you can add new fields easily. Protected class in the same file with *Memento suffix is convention used in OpenCoeli. 

And now last stone is needed: config store bean. I will skip its interface (all public methods)



	package org.opencoeli.context.config;

	import java.io.File;
	import java.io.FileInputStream;
	import java.io.InputStream;

	import org.opencoeli.utils.XStreamSerializationUtil;

	import org.apache.commons.logging.Log;
	import org.apache.commons.logging.LogFactory;

	public class HomeFolderConfigStore implements CoeliConfigStore {

    static final String CONFIG_DIR = ".opencoeli"+File.separator+"config";

    static final String EXTENSION = ".xml";

    private static final Log LOG = LogFactory.getLog(HomeFolderConfigStore.class);

    File configDir;

    public void init() {
        if(configDir == null){
            configDir = new File(System.getProperty("user.home") + File.separator + CONFIG_DIR);

            if (!configDir.exists()){
                if(LOG.isInfoEnabled())
                    LOG.info("Config dir not found, creating new "+configDir);
                configDir.mkdirs();
            }
        }
    }

    public void restorePersistable(CoeliPersistable persistable) {
        init();
        File configFile = getConfigFile(persistable);
        Object memento = null;
        if (configFile.exists())
            try {
                InputStream in = new FileInputStream(configFile);
                memento = XStreamSerializationUtil.deserialize(in);
                in.close();

            } catch (Exception e) {
                String msg = "Can not read config from file " + configFile;
                if(LOG.isWarnEnabled())
                    LOG.warn(msg, e);
                // failed, send null
            }            
        if(memento!=null)  
            persistable.restoreState(memento);
    }


    public void savePersistable(CoeliPersistable persistable) {
        init();
        Object memento = persistable.saveState();
        if(memento == null){
            if(LOG.isWarnEnabled())
                LOG.warn(persistable+ " did not return any memento on saveState()");
            return;
        }
            
        File configFile = getConfigFile(persistable);
        XStreamSerializationUtil.serialize(memento, configFile);        
    }


    public void dispose() {
        configDir = null;
    }

    private File getConfigFile(CoeliPersistable persistable) {
        String id = persistable.getPersistenceID();
        if (id == null)
            id = persistable.getClass().getCanonicalName();
        id += EXTENSION;

        File configFile = new File(configDir.getPath() + File.separator + id);
        return configFile;
    }
	}



This class stores configuration in `~/.opencoeli` folder. Config is stored in one file per class, file name is derived from class name (or persistenceID). Configuration is not restored in case config is not found, so context should define reasonable default values. This file have also some dependencies on OpenCoeli utils, but it is easy to digg it from source code. 

And now small bonus: this class is "Spring configuration restorer". It checks all beans shortly after creation and if possible restore their configuration. Only one down side is that you must use lazy bean initialization on Spring framework. I am also not sure with its robustness. 



	package org.opencoeli.context.config;

	import org.apache.commons.logging.Log;
	import org.apache.commons.logging.LogFactory;
	import org.opencoeli.context.CoeliContext;
	import org.springframework.beans.BeansException;
	import org.springframework.beans.factory.config.BeanPostProcessor;

	/**
	 * this bean post process all newly created beans shortly after initialization and 
	 * restore configuration if thei support it 
	 */
	public class SpringConfigRestorer implements  BeanPostProcessor{

	    private static final Log LOG = LogFactory.getLog(SpringConfigRestorer.class);

	    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        	//do nothing, all is done before initialization
	        return bean;
	    }

	    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        	if(bean instanceof CoeliPersistable){
	            if(LOG.isDebugEnabled())
        	        LOG.debug("Restoring config for bean "+beanName +" - "+ bean);
	            CoeliContext.restorePersistable((CoeliPersistable)bean);
	        }
        
        	return bean;
	    }

	}




Note: OpenCoeli is under GPLv2, but samples in this article are published under BSD licence.
