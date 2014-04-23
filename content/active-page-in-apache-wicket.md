Date: 2014-03-25
Title: Active Page in Apache Wicket
Tags: wicket
Category: Blog
Slug: active-page-in-apache-wicket
Author: Eldelshell

A few days ago I started a new project with Apache Wicket and I'm pretty sure I'll 
be posting some cool stuff I'll be learning during the following days using 
this framework (a nice review in the future?).

Anyway, something I found quite annoying to do and that took me some time to get a 
hold of was telling a menu which the active item is so that we can highlight it.

Basically, you'll probably have some sort of ListView with some custom MenuItem objects and a 

~~~html
<li wicket:id="myMenuElements">
~~~

Also, you'll probably have a _BasePage_ template for the layout which your 
pages will extend. The trick here is to have your _BasePage_ class constructor
to require the parameters and the active class.

~~~java
public BasePage(PageParameters parameters, Class<? extends Page> active){
    add(new MyHeader(active));
}
~~~

This way, when extending this class, you're forced to call the super constructor:

~~~java
public HomePage(PageParameters params){
    super(params, HomePage.class);
    ...
}
~~~

Finally, and if your _MenuItem_ uses _BookmarkablePageLink_ for somewhere in your _MenuItem_ code you can do something like:

~~~java
final BookmarkablePageLink link =
    new BookmarkablePageLink("menuLink", obj.getUrl());

link.add(new Label("menuLabel", obj.getTitle()));   
if(obj.getUrl().equals(this.active)){
    item.add(new AttributeModifier("class", "active"));
}
~~~

One thing to note is that the `getPage().getPageClass()` method cannot be called until 
the component has been added to the page, so we can't use that from any code that is executed in the constructors.

Hope this helps some wicket n00bz like myself :-)
