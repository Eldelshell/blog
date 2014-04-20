Date: 2012-10-17
Title: Play Framework 2.0.x JavaScript Internationalization
Tags: Java, Play!, JavaScript
Category: Blog
Slug: play-framework-20x-javascript
Author: Eldelshell

Play framework provides a very neat way of producing internationalized sites 
using the Messages plugin, but, it only supports native (Scala/Java) code 
or HTML templates, this means that JavaScript code can't be made i18n compliant.

Since this was getting on my nerves I started looking into alternatives for 
JavaScript i18n support. My first try was with [i18next](http://i18next.com/) but the JSON file 
format used wasn't something that fit with us since we already have 
all our i18n text in standard Play form in _conf/messages.xx_

Luckily, the [jquery-i18n-properties](http://code.google.com/p/jquery-i18n-properties/) jQuery 
plugin uses standard Java properties file format and that's what we're going to use here.

So, first of all, download the plugin and add it to your HTML template (right below jquery) and use the following code:

```JavaScript
$(document).ready(function(){
	$.i18n.properties({
		name: 'messages',
		path: '/i18n?',
		mode: 'map',
		cache: true,
		language: 'kk'
	});
   
	alert($.i18n.prop('label.hello.world'));
});
```

With this the plugin get's loaded and an alert is loaded to test everything works ok. Next, create a controller like:

```java
// the routes file
GET /i18n controllers.JavaScriptController.i18n()
 
// the controller
public class JavaScriptController extends Controller {
    public static Result i18n(){
        Lang l = request().acceptLanguages().get(0);
        String properties = "";
        // you can also use commons-io
        try(InputStream in = Thread.currentThread().getContextClassLoader().getResourceAsStream("messages." + l.code())){
            properties = new java.util.Scanner(in).useDelimiter("\\A").next();
        } catch (NoSuchElementException | IOException e) {
            Logger.error("Failed to read messages file");
        }
        return ok(properties).as("text/plain");
    }
}
```

Basically what we're doing here is providing a path to the plugin and using 
the standard Play language implementation, load the messages file and return it as plain text.
