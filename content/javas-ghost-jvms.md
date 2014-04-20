Date: 2011-10-19
Title: Java's Ghost JVMs 
Tags: Java
Category: Blog
Slug: javas-ghost-jvms
Author: Eldelshell

It's a nice day when you end up digging through some of the JDK source code to find out what is broken with one of the JDK tools like JPS or JConsole. Today was one of those days.

The problem was with our JBoss monitoring tool which depends on jconsoles LocalVirtualMachine.getAllVirtualMachines() method. For some reason, after a controlled restart of the farm, a couple of servers were being reported as offline. Looking at the log files, I was able to see that the PID for this servers was wrong and the process couldn't connect to retrieve the data (this is done using JMX).

The solution was to see what this method was doing with the source code from [LocalVmManager.java](http://www.java2s.com/Open-Source/Java-Document/6.0-JDK-Modules-sun/jvmstat/sun/jvmstat/perfdata/monitor/protocol/local/LocalVmManager.java.htm) and [PerfDataFile.java](http://javasourcecode.org/html/open-source/jdk/jdk-5.0/sun/jvmstat/perfdata/monitor/protocol/local/PerfDataFile.java.html)

So how does tools like JPS, JConsole or VisualVM know the JVMs running in a system? They simply look in the folder `/tmp/hsperfdata_foo` where a 32KB data file with the PID as name is created for each JVM.

![](|filename|/images/screenshot_215.png)

Back to our problem. After the restart, some of the files that should have been removed when the JVM was killed were still there, so this was giving the monitoring process a wrong PID and it couldn't connect to the JVM and do its magic.

Solution: remove the unused files and everything works as expected.

So, the next time you need to know all the JVM running on your system, remember this: `$ls /tmp/hsperfdata_*/`
