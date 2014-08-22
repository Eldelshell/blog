Date: 2010-06-01
Title: Java Template Engines, fight!
Tags: Java
Category: Blog
Slug: java-templates-2010
Author: Eldelshell


One of the greatest features Java provides for enterprise applications, are the many
frameworks, libraries and tools provided by many third-party developers. In the web development
front, we find many useful resources and today I'm gonna compare the most popular template
systems a Java developer will find.

A template system is comprimised of three main components:

* Template Engine
* Content Resource
* Template Resource

You can find more information about the theory behind template systems 
in the [Wikipedia Entry.](http://en.wikipedia.org/wiki/Web_template_system)

Our candidates are:

* FreeMarker
* Velocity
* StringTemplate
* MVEL

## FreeMarker

License: *BSD-style*

Tested Version: *2.3.16*

Dependencies: *None*

### Advantages:
* XML/HTML Templates (no need to learn a new language).
* Very simple and straight to the point.
* Plugins for lots of IDEs.

### Disadvantages:
* Latest version is almost 8 months old.
* Simplicity comes at a price: not as powerful as the others.

As stated on the projects' site _"It simply generates text"_ and it does it greatly. It was 
very easy to get to work with it and appart from the example below, I was able to generate
SQL queries, HTML pages and Configuration files, from a file or from in-code templates 
without a problem. Also, having the ability to provide an OutputWriter was great.

~~~java
public class FreemarkerExample extends TemplateExample{

    Configuration config = new Configuration();
    Template freemarkerTemplate;
    OutputStreamWriter output = new OutputStreamWriter(System.out);
    
    Map<String,String> dataModel = new HashMap<String,String>();
    
    public FreemarkerExample(String user){
        this.user = user;
        dataModel.put("user", this.user);
    }
    
    @Override
    public void print() {
        try {
            freemarkerTemplate = new Template(
				"Template", 
				new StringReader("Hello Freemarker, I'm ${user}\n"),
				config
			);
            freemarkerTemplate.process(this.dataModel, this.output);
        } catch (TemplateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        
    }

    @Override
    public void printFromFile() {
        try {
            freemarkerTemplate = config.getTemplate("templates/freemarker.xml");
            freemarkerTemplate.process(this.dataModel, this.output);
        } catch (TemplateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
~~~

## Velocity Engine

License: *Apache*

Tested Version: *1.6.4*

Dependencies: *None*

### Advantages:
* Very alive. This version is from a few weeks back.
* The most powerful.
* Most popular.

### Disadvantages:
* Ugly syntax.
* Complex.

Without a doubt, the most powerful and complex project. If you take into account 
all the parts that conform Velocity (Engine, Tools, DVSL, Texen, Anakia, etc.) you have almost
all of your needs covered. If you take only the Velocity Engine, you'll want to rip 
your eyes off because of the syntax. Also, the variable names are very easy to
get lost inside complex pieces of code, and when we're talking about velocity, they will.

I really wish they followed Python's way with the syntax. Instead of using all those counter 
intuitive pound signs. I mean, for any Unix/Linux user, those are comments
and believe me, your mind won't get used to them, ever!

It was the hardest to get running and creating a new context can be a mess in big 
systems when developers start putting data in there.

~~~java
public class VelocityExample extends TemplateExample {

    VelocityEngine engine = new VelocityEngine();
    VelocityContext context = new VelocityContext();
    
    public VelocityExample(String user) {
        this.user = user;
        context.put("user", this.user);
    }
    
    @Override
    public void print() {
        StringWriter writer = new StringWriter();
        StringReader reader = new StringReader("\nHello Velocity, I'm $user\n");
        try {
            Velocity.evaluate(context, writer, this.user, reader);
            System.out.println( writer.toString() ); 
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void printFromFile() {
        StringWriter writer = new StringWriter();
        try {
            Template template = engine.getTemplate("templates/velocity.vm");
            template.merge( context, writer );
            System.out.println( writer.toString() ); 
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
~~~

## StringTemplate

License: *BSD*

Tested Version: *3.2.1*

Dependencies: *ANTLR*


### Advantages:
* Powerful and simple
* Not limited to Web.
* Not a Java only project.

### Disadvantages:
* Counter-intuitive usage of the dollar sign.
* Single person project. Not much activity.
* Not much documentation.
* No IDE plugins

Watching an article about StringTemplate is what drove me into writing this post. 
I thought: "_finally someone is implementing a StringBuilder that behaves like it should_". But 
no, it was another template engine, but I wanted to see how it works. And it was fast and 
easy to learn, but the way the the dollar sign is used kept me head banging on the table. 

You only have to take a look at this to cry: `$if(title)$<title>$title$</title>$endif$`.

Now imagine a thousand lines of it.

If you get used to this syntax, having a template engine that works in several programming languages is a very good thing.

~~~java
public class StringTemplateExample extends TemplateExample{
	
	StringTemplate template = new StringTemplate("Hello StringTemplate, I'm $user$");
	
	public StringTemplateExample(String user) {
		this.user = user;
		template.setAttribute("user", this.user);
	}
	
	@Override
	public void print(){
		System.out.println(template);
	}
	
	@Override
	public void printFromFile(){
		StringTemplateGroup templateGroup = new StringTemplateGroup("xml group", "templates");
		StringTemplate xmlTemplate = templateGroup.getInstanceOf("xml");
		xmlTemplate.setAttribute("user", this.user);
		
		System.out.println(xmlTemplate.toString());
	}
}
~~~

## MVEL2

License: *Apache 2.0*

Tested Version: *2.0.17*

Dependencies: *None*

### Advantages:
* Easiest to use of all
* Nice syntax
* Very alive. Latest version is from March 2010

### Disadvantages:
* The eval method should accept a File object directly.
* No IDE plugins

I really liked MVEL2 for its simplicity and power. You get a very nice template 
engine and a very nice expression language which will look very familiar to 
Java programmers. No weird syntax and the usage of @{var} was a good decision 
since it's not something you see in any other place, allowing the programmer 
to easily adjust to the engine.

~~~java
public class MVELExample extends TemplateExample{

    Map<String,String> map = new HashMap<String,String>();

    public MVELExample(String user) {
        this.user = user;
        map.put("user", user);
    }
    
    @Override
    public void print() {
        System.out.println((String)TemplateRuntime.eval("Hello MVEL, I'm @{user}\n", map));
    }

    @Override
    public void printFromFile() {
        try {
            System.out.println(TemplateRuntime.eval(new FileInputStream(new File("templates/mvel.xml")), map));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}
~~~

## Conclusion

For an enterprise system the decision is clear: *Velocity*. It's the most known and 
powerful tool of them all. It might also have the ugliest syntax but if you 
get your mind around it and install your IDE plugin, things start looking 
better. If Velocity wasn't the most known of them all, I would definitely go 
with MVEL2 for everything, from complex systems to simple ones. From Web apps, to Swing apps.
