Date: 2011-10-05
Title: My Logback.xml template
Tags: Java, logback, slf4j
Category: Blog
Slug: my-logbackxml-template
Author: Eldelshell
Summary: This is a simple working XML configuration to start using Logback on your Java projects as fast as possible.

This is a simple working XML configuration to start using Logback on your Java projects as fast as possible.

~~~xml
	<?xml version="1.0" encoding="UTF-8"?>
	<configuration debug="false">
	   
	  <!-- Console -->  
	   
	  <appender name="S" class="ch.qos.logback.core.ConsoleAppender">
		<encoder>
		  <pattern>%d{yyyy-MM-dd HH:mm:ss} %c{1} [%p] %m%n</pattern>
		</encoder>
	  </appender>
	 
	  <!-- HTML Rolling Appender -->
	 
	  <appender name="H" class="ch.qos.logback.core.rolling.RollingFileAppender">
		<file>logs/jongo.html</file>
		<encoder class="ch.qos.logback.core.encoder.LayoutWrappingEncoder">
			<layout class="ch.qos.logback.classic.html.HTMLLayout">
				<pattern>%msg%n</pattern>
			</layout>
		</encoder>
		<rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy">
		  <fileNamePattern>logs/jongo.html.%i</fileNamePattern>
		  <minIndex>1</minIndex>
		  <maxIndex>3</maxIndex>
		</rollingPolicy>
		<triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy">
		  <MaxFileSize>1024KB</MaxFileSize>
		</triggeringPolicy>
	  </appender>
	 
	  <!-- Plain Text Rolling Appender -->
	 
	  <appender name="R" class="ch.qos.logback.core.rolling.RollingFileAppender">
		<Append>true</Append>
		<File>logs/jongo.log</File>
		<encoder>
		  <pattern>%d{yyyy-MM-dd HH:mm:ss} %c{1} [%p] %m%n</pattern>
		</encoder>
		<rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
		  <fileNamePattern>logs/jongo.log.%d{yyyy-MM-dd}</fileNamePattern>
		  <maxHistory>30</maxHistory>
		</rollingPolicy>
	  </appender>
	 
	  <!-- An specific Appender for Performance logs -->
	 
	  <appender name="PERF" class="ch.qos.logback.core.rolling.RollingFileAppender">
		<Append>true</Append>
		<File>logs/performance.log</File>
		<encoder>
		  <pattern>%d{yyyy-MM-dd HH:mm:ss} %c{1}:%L [%p] %m%n</pattern>
		</encoder>
		<rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
		  <fileNamePattern>logs/performance.log.%d{yyyy-MM-dd}</fileNamePattern>
		  <maxHistory>10</maxHistory>
		</rollingPolicy>
	  </appender>
	 
	  <!-- All the logs called with LoggerFactory.getLogger("performance") will go trough this logger -->
	  <logger name="performance" level="DEBUG" additivity="false">
		<appender-ref ref="PERF"/>
	  </logger>
	 
	  <logger name="org.w3c.tidy" level="OFF"/>
	  <logger name="ch.qos" level="OFF"/>
	  <logger name="org.slf4j" level="OFF"/>
	 
	  <root level="DEBUG">
		<appender-ref ref="S"/>
	<!--    <appender-ref ref="H"/>-->
	<!--    <appender-ref ref="R"/>-->
	  </root>
	</configuration>
~~~

Simply copy/paste this to your logback.xml file and it should work but you should modify it to make it work as you please.
