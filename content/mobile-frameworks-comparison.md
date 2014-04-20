Date: 2012-06-04
Title: Mobile Frameworks Comparison
Tags: Mobile, Frameworks
Category: Blog
Slug: mobile-frameworks-comparison
Author: Eldelshell

I've been studying different mobile frameworks for different projects I'm currently engaged in and this is the [result][].

How did I confront this quest of long hours of surfing the web, coding and ripping my hair? Well, 
first thing was to download all the JS files, code a simple REST backend with the [Play](http://www.playframework.org/) framework 
(a post about it is in my todo list) and setup the project while I figure out what were the criteria to follow.

If you're on your own quest for touch nirvana, the best place to start is at [Markus Falk's website](http://www.markus-falk.com/mobile-frameworks-comparison-chart/). It's simply great and will give you a starting point and get a list of contenders. In our case, the contenders list is the following:

* JQuery Mobile
* Sencha Touch 2
* The M Project
* JO
* iUI
* DHTMLX Touch
* Wink
* Bootstrap + jQuery + AngularJS

The last option I call it the "light" one. Bootstrap is great on doing what it does, showing content which adjust it self to the screen size and it offers a lot of controls which can be easily modifiable and work flawlessly in tablets and smartphones. The thing I like the most of this approach is that I feel we won't be too tied to a framework, which allows us to support more platforms. Let's see how it goes.

## The criteria

* Latest Published Version
* Supported Platforms
* Supporter
* License
* Paid Support
* Documentation (API, Examples, Tutorials)
* Published Books
* Community
* Stack Overflow Questions
* Google Trends Popularity
* GUI Designer
* Theme Designer
* HTML5 Input support
* Hides browser navigation bar
* Geolocalization Support
* Custom controls
* International support (i18n)

I had most of the information I needed, so now and start the tests. Our prototype application won't be too complicated, but I wanted to see how the different frameworks handled long lists of grouped items. 

## The web-app

I can't show all screenshots of the prototypes I'm developing because it's a work in progress, but basically the each one will have three "views": 

* Landing (with some nice effect if possible)
* Form with the following widgets
* Autocomplete
* Spinner
* Datepicker
* Collapsible blocks
* Results view which is a very long (1000) list of grouped items

To check the performance I did the tests with:

* Safari - iPhone 4S - IOS 5
* Safari - iPhone 3GS - IOS 5
* Google Chrome - Samsung Galaxy S - Android ICS
* Stock Browser - Samsung Galaxy SII - Android Gingerbread

## jQuery Mobile

jQuery Mobile seems to be the most popular around and the only inconvenience I found when using the "kitchensink" was performance on the SMGS. Using the excellent tools, I got the app up and running, even with the theme colors for the target brand in no more than two hours, with some nice effects and all.

Performance was really good even when not using the minified version and the only caveat was with the "slide" effect which brought the SMGS to its knees. Not a problem with the other phones even with all effects. The nested list handled fine all the amount of items we needed. The general experience was excellent and I really liked JQM. The other frameworks are going to have a hard time beating it.

![](|filename|/images/Selection_003.png)

### Pros

* Great tools like Theme Roller and Codiqa UI builder.
* View only framework (you can use whatever to handle the MC parts)
* Based on jQuery
* Lots of plugins (I specially liked the Swipe menu)
* Most popular

### Cons

* Could be too heavy for some smartphones.
* No official paid support.

## Sencha Touch 2

I stumbled with Sencha Touch some time ago while reviewing ExtJS for another kind of project. And ExtJS is great, Sencha Touch not so much. Luckily I had the experience of working with the framework and its MVC architecture but if it's your first time around with ExtJS you'll have to do some learning.

Setting up the application took more work than with jQuery Mobile because I had to download, install and setup "Sencha Architect" but after this it was pretty straight forward. Note that you don't need this tool to develop with this framework, but I didn't want to waste my time moving "divs" around.

Sencha Architect was really helpful, but I couldn't make the webapp look as I wanted it and some things really started to frustrate me, like placing the button icons on the right side. Here's a screenshot of pretty much what I started with.

Finally I gave up on the UI and started to code to see if I could get the same functionality than with jQuery Mobile. And here I stumbled into my first serious problem. All the components are defined with JavaScript code. This works well for RIA, but for mobile I don't think it's the best to have the mobile browser do all the heavy lifting.

Finally and after more hours than it deserved I got the prototype "working". At first sight the application performed very well in iOS, but when I threw the list of items, not even the iPhone 4S was able to handle it. I believe the binding of all this data in the Stores and the view was killing it. With Android it was a whole different story because the performance was really poor and clicking on an item of the list selected the whole screen instead of launching a click event. This might have been a bug in Sencha Architect, but I'm not sure.

Another issues I had with Sencha Touch 2 were:

* Some buttons looked very low quality
* The controls (i.e. the input type 'date') weren't the native ones
* No easy way to change the default theme
* Impossible to customize controls like button icons.
* Architect doesn't allow to add the "data" field to Stores making it hard to preview lists

In general, I didn't like the experience at all compared with jQuery Mobile which took me a few hours to almost have a completely functional webapp.

![](|filename|/images/Selection_002.png)

### Pros

* Based on ExtJS
* Complete MVC framework
* Official paid support
* Sencha Architect is great

### Cons

* Some controls look off
* No native controls
* Performance
* Few customization options
* Client side DOM generation

## DHTMLX Touch

I've never used DHTMLX before, but the premise seems to be the same than with ExtJS: a MVC framework for RIA. And again I don't think this will work well for us on the mobile front. First, the Online Visual Designer wasn't helping me at all. For some reason it kept doing weird things. For example, try to add a "richlist" or "combobox" after you've added a datepicker. Everything is gone!

This got me frustrated really fast, so I tried to work out the prototype cowboy style, with code. At least one thing which I thought was a good idea apart from Sencha was that the controls are defined separately with the ui function. This was the result:

Not great. But one thing got my attention and it was the performance. It was really fast loading and handling animations on the SMGS and iPhone 3GS.

As with Sencha Touch, I didn't like the experience very much. The general feeling is of a beta product, beginning with the UI designer. Getting started was easier than with Sencha but then things went downhill as my lack of knowledge of how things work with DHTMLX started to show.

![](|filename|/images/Selection_005.png)

### Pros

* Based on DHTMLX
* Complete MVC framework
* Official paid support
* Very good performance and resource usage.

### Cons

* Some controls look off, like the counters are too big.
* No native controls
* No icons in the buttons
* Client side DOM generation
* The UI designer
* Very few customization options

To be continued!

[result]: https://docs.google.com/spreadsheet/ccc?key=0Ap3IHeZltVF-dEM3VW9CMml0VURnSXhwMU5hZW9CQ1E
