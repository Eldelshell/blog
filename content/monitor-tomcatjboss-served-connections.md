Date: 2011-05-12
Title: Monitor Tomcat/JBoss served connections
Tags: Java, Tomcat, JBoss
Category: Blog
Slug: monitor-tomcatjboss-served-connections
Author: Eldelshell

Say you want to monitor how many connections each of your JBoss/Tomcat servers are serving, because, you might want to make sure load balancing is working correctly. This can be accomplished by reading this information from an MBean, in this case the GlobalRequestProcessor.

![jconsole screenshot of a jboss jvm](|filename|/images/screenshot_179.png)

The image speaks by itself. So, depending on how your Tomcat server is being accessed, you can count the number of served requests it has processed and many more data which could become useful someday.
