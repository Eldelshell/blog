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

For explicit unique objects it might not be a big deal, but when you write some utility function (which you will)
like `toString` you'll wish you started to emulate namespaces:

~~~vb
' File stringUtils.brs
' You could write this
function toString(any as Dynamic) as String
    ...
end function

' Or keep some order
function StringUtils() as Object
    return {
        toString: function(any as Dynamic) as String
            ...
        end function
    }
end function
~~~

Now you can have a `toString` for native types (integers, booleans, etc), for collections (array, associative array) and for different objects, for example:

~~~vb
' You'll write this one for sure
function DateUtils() as Object
    return {
        toString: function(date as Object) as String
            ...
        end function
    }
end function
~~~

A good example of BrightScript™ code is the _customvideoplayer_ example in the SDK. You'll want a more OO aproach:

~~~vb
function getMyPage() as Object
  return {
    screen: createObject("roScreen"),
    port:   createObject("roMessagePort"),
    
    setup: function() as Void
      m.screen.setMessagePort(m.port)
    end function,
    
    eventLoop: function() as Void
        while true
            msg = wait(0, m.port)
        end while
    end function
    
    show: function() as Void
      m.screen.show()
      m.eventLoop()
    end function
  }
end function
~~~

### toString
This is one of the first functions you'll want to write and to do it right because BrightScript doesn't like code you take for granted in other languages, like string concatenations:

~~~vb
print "This is a String" + 1
' Will fail with a Type error
~~~

So, your `StringUtils().toString(any)` function should be able to take anything and be able to convert it to a string which you can later use to print/debug stuff.

### Always wait()

As you can see in my code above, I used the global function `wait()` which is described in the documentation as

> returns the event object that was posted to the message port. If timeout is zero, "wait" will wait for ever. Otherwise, Wait will return after timeout milliseconds if no messages are received. In this case, Wait returns a type "invalid".

You don't want to make the mistake of doing `msg = m.port.getMessage()` and leave that `while` loop running like crazy. Better to `wait()` for the events.

### Debugging

Here's the deal with debugging: it doesn't work. We were working with the newest firmwares and the debugging console didn't work. So, you're left with doing the old-school debugging technic of using logs.

### Logging

If your first function is `toString()` your second one will be a proper logger, because you don't want to use `print` or `?` and later on remove all of them or some of them. Here's my take at a logger:

~~~vb
' Usage:
' l = getLogger("MyPage.brs")
' l.info("Hello {0}", "World")
' Result:
' [01-12-2014 00:00:00.100] [INFO] [MyPage.brs] Hello World
function getLogger(parent as String) as Object
    logger = {
        date:   createObject("roDateTime"),
        parent: parent,
        level:  0,
        format: "[{0}]" + chr(9) + "[{1}]" + chr(9) + "[{2}]: {3}",
        
        setup: function() as Void
            m.date.toLocalTime()
        end function
        
        log: function(str as String, level as String) as Void
            print substitute(m.format, m.getTimestamp(), level, m.parent, str)
        end function
        
        info: function(str as String, a = Invalid as Dynamic, b = Invalid as Dynamic) as Void
            if m.level >= 2 then
                msg = substitute(str, StringUtils().toString(a), StringUtils().toString(b))
                m.log(msg, "INFO")
            end if
        end function
        
        getTimestamp: function() as String
            m.date.mark()
            timeStamp = m.date.asDateString("short-date-dashes")
            timeStamp = timeStamp + " " + m.date.getHours().toStr()
            timeStamp = timeStamp + ":" + m.date.getMinutes().toStr()
            timeStamp = timeStamp + ":" + m.date.getSeconds().toStr()
            timeStamp = timeStamp + "." + m.date.getMilliseconds().toStr()
            return timeStamp
        end function
    }
    logger.setup()
    return logger()
end function
~~~

### Testing

If you're used to fancy testing frameworks like jUnit or Mockito, you're out of luck with BrightScript. This doesn't mean you shouldn't do unit testing, but that it will require some scripting magic. If you're using the `app.mk` make file from the SDK (which is the best thing to use to build and deploy your channel to the hardware) modifying your source code to run your tests shouldn't be too hard. You could, for example, modify the make script to modify your `main` function to run your tests before the channel's code. Something like:

~~~vb
' main.brs
sub main(args as Dynamic)
    doTests = [TEST_TAG] ' value changed via make + sed -i s/[TEST_TAG]/true/ source/main.brs
    
    if doTests then runAllTests()
    
    ' Continue to channel code
    ...
end sub
~~~

### Editors

While this project lasted I used VIM and jEdit. For VIM you can download the syntax highlight file from Roku's site. For jEdit you can reuse the one of VisualBasic and modify it a little to BrightScript needs.

I could get the Eclipse plugin to work, so don't waste more than a few minutes with it if it doesn't work at first.

My coworkers used Sublime Text which worked quite well too. I also tried with gEdit and it too worked quite fine.

### Miscellaneous

 * Always call `date.toLocalTime()` after you instantiate a new `roDateTime`.
 * Reuse the `roUrlTransfer` object for faster connections.
 * Add all required headers to HTTP connections.
