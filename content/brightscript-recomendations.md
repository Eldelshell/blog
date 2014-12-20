Date: 2014-12-20
Title: A jQuery Mobile Progress Bar
Tags: Roku, BrightScript
Category: Blog
Slug: brightscript-recomendations
Author: Eldelshell

I've just finished a big project for the Roku™ streaming hardware. It uses a language called BrightScript™
which is sort of a mix between VisualBasic and JavaScript. This are my recomendations when starting a new
project for this platform.

## Global Scope

When you start developing for the Roku™ you'll download their SDK and look out for the examples looking for
an easy _Hello World_ to start with. Or you'll look the examples in the documentation. And here comes my first
recomendation, don't follow the style of those examples.

You'll probably find code that looks like this:

~~~vb
sub showMyPage()
    screen = createObject("roScreen")
    port = createObject("roMessagePort")
    screen.setMessagePort(port)
    screen.show()
    
    while true
        msg = wait(0, port)
        ...
        
    end while
end sub

function otherFunction() as String
  return "Hello World"
end function
~~~

My first recomendation is, don't do this. Don't put all your code in functions on the global scope or you'll
hit with some _features_ of BrightScript:

 * No namespaces (like JavaScript)
 * Functional (like JavaScript)
 * Case insensitive (like Visual Basic)

A good example of BrightScript™ code is the _customvideoplayer_ example in the SDK. You'll want a more OO aproach:

~~~vb
function getMyPage() as Object
  return {
    screen: createObject("roScreen"),
    port:   createObject("roMessagePort"),
    
    setup: function() as Void
      m.screen.setMessagePort(m.port)
    end function
    
    show: function() as Void
      m.screen.show()
    end function
  }
end function
~~~
