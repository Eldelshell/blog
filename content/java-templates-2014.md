Date: 2014-08-23
Title: Java Template Engines 2014 edition
Tags: Java
Category: Blog
Slug: java-templates-2014
Status: draft
Author: Eldelshell

Four years ago I made a comparison of some template engines for Java. A few days ago
I received a comment in the old blog commenting about some new one and since I was also
involved in using a template engine in a personal project, I decided to revisit this
article.

Our candidates are:

* FreeMarker
* [Velocity](http://velocity.apache.org/)
* StringTemplate
* [Rythm](http://rythmengine.org/)
* [MVEL2](http://mvel.codehaus.org/)

## MVEL2

License: *Apache 2.0*

Previously tested version: *2.0.17*

Currently tested version: *2.2.1*

Dependencies: *None*

### Advantages:
* Easy to use.
* Very alive. Latest version is from Apr 17 2014.

### Disadvantages:
* The eval method should accept a File object directly.
* No IDE plugins.
* Documentation is awful and outdated.

Last time this was my option for small projects but now we have lots of
contenders. Either way, MVEL2 is still very easy to use and the code I used
in 2010 still worked with the new version. Since then I've used many other
engines, like Jinja2 for Python and using MVEL2 syntax (`@{my_string}`) got
to be a little painful. 

## Velocity

License: *Apache*

Previously tested version: *1.6.4*

Currently tested version: *1.7*

Dependencies: *Commons Collections & Commons Lang*

### Advantages:
* The most powerful.
* Almost every Apache project has a plugin for Velocity.
* Most popular.

### Disadvantages:
* Ugly syntax.
* Complex.
* Kind of outdated since the last version is from 2010.

Things haven't changed a lot since 2014 regarding Velocity. It's still the most
complex, powerful and [recommended template engine](http://stackoverflow.com/questions/3793880/lightweight-template-engine-in-java) for JEE. No wonder you can find a Velocity plugin/module/whatever for almost anything:

* Spark
* Cocoon
* Camel
* Play
* Solr
* Tiles
* Wicket
* SpringMVC

## 
