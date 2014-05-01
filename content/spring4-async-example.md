Date: 2014-04-01
Title: Spring 4 @Async usage example
Tags: Java, Spring
Category: Blog
Slug: spring4-async-example
Author: Eldelshell

Here's a fast example to get you started up with using asynchronous tasks with the `@Async`
annotation from Spring.

This are our dependencies:

~~~xml
<dependency>
	<groupId>org.springframework</groupId>
	<artifactId>spring-context</artifactId>
	<version>4.0.3.RELEASE</version>
</dependency>
~~~

We'll be using annotations mixed with XML so we reach the most with this little example. So
now we need our _spring.xml_ file:

~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:task="http://www.springframework.org/schema/task"
       xsi:schemaLocation="
            http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/context
            http://www.springframework.org/schema/context/spring-context-4.0.xsd
            http://www.springframework.org/schema/task
            http://www.springframework.org/schema/task/spring-task-4.0.xsd">
            
    <context:annotation-config />
    <context:component-scan base-package="osuya.example"/>
    
    <task:annotation-driven />
    
    <bean class="osuya.example.Spring4Tasks" name="spring4Tasks"></bean>
</beans>
~~~

The important parts here are __XSD__ definitions for the _task_ namespace and the
`<task:annotation-driven />` that tells spring to scan our components for the `@Async` and
`@Scheduled` annotations.

I'll write about the `@Scheduled` annotation in the future and how it might be useful.

Finally, we'll create two `@Service` components:

* NormalService + NormalServiceImpl
* ASyncService + ASyncServiceImpl

Here's the code for the __ASyncServiceImpl__ which has the important parts:

~~~java
package osuya.example;

import java.util.concurrent.Future;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Service;

@Service
public class ASyncServiceImpl implements ASyncService {
	
	@Autowired NormalService normalService;

	@Async
	@Override
	public Future<Boolean> async() {
		
		// Demonstrate that our beans are being injected
		System.out.println("Managed bean injected: " + (normalService != null));
		
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		System.out.println("I'm done!");
		
		return new AsyncResult<Boolean>(true);
	}

}
~~~

So, for a method to work asynchronously we need to annotate it with `@Async` and have it
return an `AsyncResult`.

Now, let's see how it works with the following code:

~~~java
package osuya.example;

import java.util.concurrent.Future;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class Spring4Tasks {

	@Autowired ASyncService asyncService;
	
	@Autowired NormalService normalService;
	
	public static void main(String[] args) {
		ApplicationContext context = new ClassPathXmlApplicationContext("/spring.xml");
		Spring4Tasks app = context.getBean(Spring4Tasks.class);
		app.start();
		System.exit(0);
	}
	
	public void start() {
		normalService.notAsync();
		
		Future<Boolean> result = asyncService.async();
		
		for(int i = 0; i < 5; i++) normalService.notAsync();
		
		while(!result.isDone()){
			// we wait
		}
	}
}
~~~

The result should be:

> Not in a thread

> Not in a thread

> Not in a thread

> Not in a thread

> Not in a thread

> Not in a thread

> Managed bean injected: true

> I'm done!

You can check the Maven project [here](https://github.com/Eldelshell/blog/tree/master/examples/spring4-async-example) and run it with:

~~~bash
$ mvn clean install exec:java -Dexec.mainClass="osuya.example.Spring4Tasks"
~~~
