Date: 2014-04-22
Title: An Apache Wicket Review
Tags: Java, Wicket
Category: Blog
Slug: a-wicket-review
Author: Eldelshell
Status: draft

For the last few weeks I've been trying out [Apache Wicket](http://wicket.apache.org). The first thing that got me into using Wicket was its Java focused features, which allowed me to use almost raw HTML and simply including `wicket:id` tags.

I have pretty much everything I need setup:

* Authentication
* i18n
* REST resources

## Java Hell

At first, the idea of only modifying the view from Java code seemed attractive, until you have to write a repeater (table, list, etc):

~~~java
public static final main(){

	private static final test = "test";

}
~~~


