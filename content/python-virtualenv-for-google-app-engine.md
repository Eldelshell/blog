Date: 2013-04-16
Title: Python virtualenv for Google App Engine and Flask
Tags: python, gae
Category: Blog
Slug: python-virtualenv-for-google-app-engine
Author: Eldelshell

Ok, this was so easy I couldn't believe it. First Download the App Engine SDK. 
Then install __virtualenv__ if you don't already have. Create a new folder, 
for example, `/opt/environments/gae` and do some virtualenv magic:

~~~bash
$ cd /opt/environments
$ mkdir my-gae
$ virtualenv my-gae

New python executable in my-gae/bin/python
Installing distribute....done.
Installing pip....done.
~~~

Great, now I installed the SDK inside the virtualenv folder:

~~~bash
$ cd my-gae
$ unzip ~/Downloads/google_appengine_1.7.7.zip
$ mv google_appengine google_appengine_1.7.7
$ ln -s google_appengine_1.7.7 gae
~~~

You should be left with something like this:

~~~bash
├── bin
├── gae -> google_appengine-1.7.7
├── google_appengine-1.7.7
├── include
├── lib
└── local
~~~

This will allow us to update our GAE SDK version without much hassle. Now let's configure 
the SDK for our new virtualenv. First, edit the file `bin/activate` to look like this:

~~~bash
PATH="$VIRTUAL_ENV/bin:$PATH"
PATH="$VIRTUAL_ENV/gae:$PATH"   # New line for GAE
export PATH
~~~

Next time you run `source bin/activate` that line will add the SDK `dev_appserver.py` executable to our path.

Finally, we need to add our path configuration for the GAE path. Create a new file `lib/python2.7/site-packages/gae.pth` with the following:

~~~python
import dev_appserver; dev_appserver.fix_sys_path()
~~~

Let's see if everything works.

~~~bash
$ cd /opt/environments/my-gae
$ source bin/activate
(my-gae)
$ dev_appserver.py
usage: dev_appserver.py [-h] [--host HOST] [--port PORT]
                        [--admin_host ADMIN_HOST] [--admin_port ADMIN_PORT]

dev_appserver.py: error: too few arguments
(my-gae)

$ python -c "from google import appengine"
(my-gae)
~~~

We're done with the GAE SDK, now let's go with Flask, which is a bit of a pain, 
specially Flask-Babel. The easiest thing to do is to use one of the already 
set up projects like [flask-appengine-template](https://github.com/kamalgill/flask-appengine-template) or [http://gae-init.appspot.com/](http://gae-init.appspot.com/) which include everything you need.

