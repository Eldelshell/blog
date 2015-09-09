Date: 2015-09-09
Title: JobHunter Chrome™ Packaged App
Tags: projects
Category: Blog
Slug: jobhunter-chrome-presentation
Author: Eldelshell

Today I added the first release of a new open source project called *JobHunter* which
is my take at trying to fix a very personal problem: managing all the jobs I've been
applying for and have a central reference from all the different job portals.

You can install it from the [Chrome Web Store](https://chrome.google.com/webstore/detail/jobhunter/gldahcpimmpidgnonlioblncljkicjak)

![JobHunter](|filename|/images/Selection_481.png "JobHunter")

## What it does?

Basically, JobHunter allows its users to add the jobs you've applied for and keep track
of the different things which happen to it, sort of a CRM but for people looking for a job.

### Jobs

The things you can keep track are:

* Job position, salary, description and rating.
* Company information.
* Contacts related to the position (HeadHunter, HR representative, etc.)
* Events like when you have/had an interview.

### Importing

At first, adding jobs one by one wasn't a problem, but then I started to search for public APIs
and luckily many job portals have a public API which can be used to import the job's data into
*JobHunter*. So I decided to add this feature which would allow people to
to import jobs from any portal with a public API or by doing some scrapping.

## How it was made?

*JobHunter* is a Chrome packaged application with the following dependencies:

* npm + grunt for the package management and build system.
* RequireJS for AMD.
* Underscore, jQuery and Backbone.
* Bootstrap + FontAwesome icons.
* RSVP for promises.
* idb-wrapper for InternetDB operations.

## Backbone

I worked with lots of JavaScript frameworks (frontend and backend) but never got the oportunity to
work with Backbone, so when I decided to port the original [JobHunter in JavaFX](https://github.com/Eldelshell/JobHunter)
to Chrome™ I didn't want to use one framework which I had already used before.

To be honest, I wanted to start with ReactJS, but the workflow with Chrome™ didn't feel quite right
and using templates with packaged apps is a no go because of Chrome™ limitation of not allowing the use
of `eval`.

This is why Backbone made perfect sense. No need to use templates. Also, the Backbone workflow and
coding style is really close to an internal framework I work with daily.

### Chrome™ Packaged Apps and RequireJS

Any JavaScript project with more than a few lines of code should be using AMD or the likes. For *JobHunter*
I took the safe way with RequireJS. At first it took a little of mangling to get it to work, but nothing really
complicated. The important part was understanding a packaged app startup flow. All this magic happens in this way.

1. Chrome loads the `manifest.json` file and from there loads the `js/chrome/main.js` file.
2. `js/chrome/main.js` creates a new window with `chrome.app.window.create` with the `index.html`.
3. The `index.html` loads `require.js` and `js/chrome/require.config.js`
4. `js/chrome/require.config.js` sets up everything and adds a few shims and mixins to _Underscore_

## Wrap up

The experience have been very productive and I find Chrome™ Packaged apps to be a great way to truly develop
_code once, run everywhere_ GUI applications. Any experienced web developer should be able to have a packaged
application ready in no time.

Now some stats as of version 0.1.2:

* LOC: 3282
* Hours: Between 20 and 24 hours
* Test coverage: 0%
