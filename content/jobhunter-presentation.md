Date: 2014-08-29
Title: JobHunter and JavaFX
Tags: projects
Category: Blog
Slug: jobhunter-presentation
Author: Eldelshell

Today I added the first release of a new open source project called *JobHunter* which
is my take at trying to fix a very personal problem: managing all the jobs I've been
applying for and have a central reference from all the different job portals.

You can download it from [Github](https://github.com/Eldelshell/JobHunter)

## What it does?

Basically, JobHunter allows its users to add the jobs you've applied for and keep track
of the different things which happen to it, sort of a CRM but for people looking for a job.

### Jobs

The things you can keep track are:

* Job position, salary, description and rating.
* Company information.
* Contacts related to the position (HeadHunter, HR representative, etc.)
* Events like when you have/had an interview.

### Plugins

At first, adding jobs one by one wasn't a problem, but then I started to search for public APIs
and luckily many job portals have a public API which can be used to import the job's data into
*JobHunter*. Instead of building *JobHunter* around this feature, I created a plugin system
which would allow people to add their own plugins to import jobs from any portal with a public API
or by doing some scrapping.

## How it was made?

*JobHunter* is a JavaFX desktop application (looking forward to make the Android version) with
the following dependencies:

* Maven 3 as build system.
* MVEL2 to generate HTML.
* XStream for the XML persistence.
* Jackson for JSON data handling (to be used by Plugins)
* Commons HttpClient (to be used by Plugins)
* jSOUP to parse HTML (to be used by Plugins)
* Reflections to load the plugins.
* ControlsFX to extend JavaFX features.

## JavaFX

First, I want to state that I wanted to do some desktop stuff, which I haven't done in a long while. Since
I've already used SWT, Swing, GTK, Qt and WxWidgets I wanted to learn something new and JavaFX would allow me
to learn two things at the same time: JavaFX and Java8 (Stream, Lambdas, etc).

The hardest part with JavaFX was setting up my Maven project to correctly execute and include all of JavaFX
libraries, but nothing a quick search wouldn't fix.

### JavaFXSceneBuilder 2.0

Using a tool like _JavaFXSceneBuilder_ made things pretty easy, and if you've ever done any GUI
applications, you won't be dissapointed that the standard stuff is there. Hell, even Android devs should
understand JavaFX in no time. Mind that _JavaFXSceneBuilder_ is kind of raw and needs lots of work 
to reach the quality of similar tools, but it really helps when working with complex layouts.

With _JavaFXSceneBuilder_ you generate *FXML* files which are later imported by your Java application. One of
the things I found to give me more flexibility was to not indicate the _controller_ in the _FXML_ file and instead
add it later when you're importing the layout:

~~~java
default Optional<Parent> load() {
	FXMLLoader fxmlLoader = new FXMLLoader(MyController.class.getResource(PATH));
	fxmlLoader.setController(this);
	try {
		return Optional.of((Parent)fxmlLoader.load());
	} catch (IOException e) {
		l.error("Failed to open file {}", PATH, e);
	}
	return Optional.empty();
}
~~~

Another great feature of JavaFX is the use of a sort of CSS (i.e. `-fx-background-color`) to handle the styling
of the application, separating concerns in three ways:

* Java code for logic.
* FXML for GUI structure.
* CSS for styling.

Every JavaFX component has its default class (i.e. `.button`) and you can add you own classes and id, so any
web developer or designer should be able to style a JavaFX application without much problem. Here _JavaFXSceneBuilder_
also help with its CSS analyzer, which works in pretty much the same way as the one in Firefox or Chrome.

### Progress bars and Worker

One of the hardest things in GUI development is progress bars, and JavaFX comes a long way to help on this
with its own threading system based on the `Worker` interface. This system gives easy threading and
good UX. As an example, this is how I handle importing a job from a remote API:

~~~java
ImportService s = new ImportService(url);
		
s.setOnSucceeded((event) -> {
	// FTW!
});

s.setOnFailed((event) -> {
	// :-(
});

Dialogs.create().message("Importing...").showWorkerProgress(s);
s.start();
~~~

The `ImportService` is an `Observer` of the class which does the connection and HTML parsing like:

~~~java
@Override
protected Job call() throws Exception {
	try{
		return Client.of(url).observe(this).execute();
	}catch(Exception e) {
		throw new MonsterAPIException("Failed to import");
	}
}

@Override
public void update(Observable o, Object arg) {
	Client.Event event = (Client.Event) arg;
	// Use Task methods to indicate the changes to the progress dialog
	updateMessage(event.message);
	updateProgress(event.position, event.total);
}
~~~

The progress dialog will pickup the events raised by our `Task` and update itself.

## Java 8

If there's something for which Java 8 new lambdas are useful are with JavaFX (or Swing for that matter):


~~~java
// With Java 8
profileController.setListener(() -> {
	// () indicates empty args
	refresh();
});

// Before Java 8
profileController.setListener(new ProfileRepositoryListener() {
	@Override
	public void changed() {
		refresh();
	}
});
~~~

I believe the reason for Lambdas is clear.

## Wrap up

The experience have been very productive and I find JavaFX to be a great way to develop GUI applications. Much of the
code noise associated with Swing is gone and code is much cleaner and easier to write thanks to Java8 new features. Also,
any new JavaFX project should include *ControlsFX* if not only for the `Dialogs` but also as a good example of creating
stuff with JavaFX. 
