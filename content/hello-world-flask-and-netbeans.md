Date: 2013-03-11
Title: Hello World Flask and NetBeans
Tags: flask, netbeans, python
Category: Blog
Slug: hello-world-flask-and-netbeans
Author: Eldelshell

Let me explain how easy it's to get started with developing a Python backend with tools as NetBeans, virtualenv and Flask.

First, download the latest version of NetBeans 7.3 PHP (this is the lightest version). After 
installing it, install the Python plugin repository:

~~~
http://deadlock.netbeans.org/hudson/job/nbms-and-javadoc/lastStableBuild/artifact/nbbuild/nbms/updates.xml.gz
~~~

_(You might also want to remove the PHP related plugins)_

After restarting NetBeans we're ready to setup our Python virtual environment. In Debian based distributions install with:

~~~bash
$ sudo apt-get install python-virtualenv
~~~

Next we setup our first environment flask-env:

~~~bash
$ mkdir python-environments
$ cd python-environments
$ virtualenv flask-env
$ cd flask-env
$ source bin/activate
$ mkdir apps
~~~

Inside flask-env you should get something like:

~~~bash
.
└── flask-env
    ├── apps
    ├── bin
    ├── include
    ├── lib
    └── local
~~~

This is fairly the same structure you'll see in Python's site-package folder.

To setup NetBeans to use the new virtualenv we'll need to create a new "Python platform" which you'll find in `Tools -> Python Platforms`.
Simply create a new platform and point it to the virtualenv python binary in `python-environments/flask-env/python/bin/python`

Finally, let's setup Flask for our Hello World example. Go back to your console were you executed source and execute:

~~~bash
(flask-env)$ easy_install Flask
~~~

Create a new Python proyect on NetBeans in the apps folder of your virtual environment and 
specify the new Python platform you just created (you can set it as default).

![Choose Project](|filename|/images/Project_025.png "Choose Project")

![Select virtualenv](|filename|/images/Project_026.png "Select virtualenv")

Copy/paste the Hello World example from Flask site, click on Run and point your browser to `http://localhost:5000/`

![Flask Server Running](|filename|/images/Selection_027.png "Flask Server Running")
