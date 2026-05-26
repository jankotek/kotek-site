+++
title = "Piccolo and SVG"
template = "page.html"
description = "I was thinking how to improve symbols on map. Star clusters, nebulas etc have complicated signs and it is difficult to draw them with plain Java2d. I decided to use SVG vector graphic to draw those symbols. Using vector editor is way way easier then coding in Java2d."
path = "blog/piccolo_and_svg"
date = 2009-11-07
[extra]
render_title = false
+++

Piccolo and SVG
======
I was thinking how to improve symbols on map. Star clusters, nebulas etc have complicated signs and it is difficult to draw them with plain Java2d.  I decided to use SVG vector graphic to draw those symbols. Using vector editor is way way easier then coding in Java2d.

<!-- more --> 

Asterope is using Piccolo 2d framework to manage map scene. But this does not support SVG yet. It is in [TODO list](http://code.google.com/p/piccolo2d/wiki/SvgSupport), but no serious implementation is done yet. 

So I wrote one. It is using lightweight SVG renderer [SVG Salamander](https://svgsalamander.dev.java.net/). It is very fast, and adds only 300kb jar to dependencies. 

I used PImage internals to see howto hook into Piccolo. Also SVGIcon was usefull to see howto paint SVG. This is first shot implementation, but already supports rotation, transformations, animations ...

Here is code with testing main method:


	package org.asterope.util;

	import com.kitfox.svg.SVGCache;
	import com.kitfox.svg.SVGDiagram;
	import com.kitfox.svg.SVGException;
	import com.kitfox.svg.SVGUniverse;
	import com.kitfox.svg.app.beans.SVGIcon;
	import edu.umd.cs.piccolo.PNode;
	import edu.umd.cs.piccolo.util.PBounds;
	import edu.umd.cs.piccolo.util.PPaintContext;
	import edu.umd.cs.piccolox.PFrame;

	import java.awt.*;
	import java.net.URI;
	import java.net.URL;


	/**
	 * Piccolo node which draws SVG using SVGIcon from SVG Salamander
 	*/
	public class PSvgNode extends PNode {

    /**
     * The property name that identifies a change of this node's SVG URI
     * Both old and new value will be set correctly
     */
    public static final String PROPERTY_IMAGE = "image";
    public static final int PROPERTY_CODE_IMAGE = 1 << 15;


    protected SVGUniverse svgUniverse = SVGCache.getSVGUniverse();

    protected URI svgURI = null;

    public PSvgNode(String resPath) {
        setSvgResourcePath(resPath);
    }

    public PSvgNode(URI svgURI) {
        setSvgURI(svgURI);
    }



    /**
     * @return the uni of the document being displayed by this icon
     */
    public URI getSvgURI() {
        return svgURI;
    }

    /**
     * Loads an SVG document from a URI.
     *
     * @param svgURI - URI to load document from
     */
    public void setSvgURI(URI svgURI) {
        URI old = svgURI;
        this.svgURI = svgURI;
        if (svgURI != null) {
            SVGDiagram diagram = svgUniverse.getDiagram(svgURI);
            if (diagram == null)
                setBounds(0, 0, 0, 0);
            else
                setBounds(0, 0, diagram.getWidth(), diagram.getWidth());
            invalidatePaint();
        }

        firePropertyChange(PROPERTY_CODE_IMAGE, PROPERTY_IMAGE, old, this.svgURI);
    }

    /**
     * Loads an SVG document from the classpath.  This function is equivilant to
     * setSvgURI(new URI(getClass().getResource(resourcePath).toString());
     *
     * @param resourcePath - resource to load
     */
    public void setSvgResourcePath(String resourcePath) {
        try {
            setSvgURI(getClass().getResource(resourcePath).toURI());
        }
        catch (Exception e) {
            throw new RuntimeException("Resource not found "+resourcePath,e);
        }
    }


    protected void paint(PPaintContext paintContext) {

        SVGDiagram diagram = svgUniverse.getDiagram(svgURI);
        if (diagram == null) return;
        double iw = diagram.getWidth();
        double ih = diagram.getHeight();
        Graphics2D g = paintContext.getGraphics();
        PBounds b = getBoundsReference();
        try {
            if (b.x != 0 || b.y != 0 || b.width != iw || b.height != ih) {
                g.translate(b.x, b.y);
                g.scale(b.width / iw, b.height / ih);
                diagram.render(g);
                g.scale(iw / b.width, ih / b.height);
                g.translate(-b.x, -b.y);
            } else {
                diagram.render(g);
            }
        } catch (SVGException e) {
            throw new RuntimeException(e);
        }
    }

    //testing method
    public static void main(String[] args){
        new PFrame(){


            
            public void initialize() {
                setSize(1000,1000);
                getCanvas().setBackground(Color.blue);
                //add your own svg resource
                PSvgNode n = new PSvgNode("/org/asterope/map/img/star.svg");

                getCanvas().getCamera().addChild(n);
                n.setOffset(500,500);
                n.animateToPositionScaleRotation(10,10,10,10,10000);
            }
        };
    }

	}
