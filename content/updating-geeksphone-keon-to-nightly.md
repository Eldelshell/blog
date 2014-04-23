Date: 2013-05-31
Title: Updating Geeksphone Keon to Nightly Build
Tags: geeksphone
Category: Blog
Slug: updating-geeksphone-keon-to-nightly
Author: Eldelshell

Tonight I decided to update FirefoxOS on my Keon, because the version that comes by default is, well, not too good enough for my nerves.

Anyway, the process is quite easy, on Linux at least.

Before you begin, be sure to have enabled the remote debugging option and at least 10% of battery in your Keon. 

Download the latest nightly build from Geeksphone and unzip it somewhere.

Now, add/edit the file `/etc/udev/rules.d/51-android.rules` with this two lines:

~~~
SUBSYSTEM=="usb", ATTR{idVendor}=="05c6", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"
~~~

Put the Keon on Airplane Mode and plug it to the computer with the USB cable.

~~~bash
./flash.sh
~~~

You should get the following output:

~~~
* daemon not running. starting it now on port 5037 *
* daemon started successfully *
< waiting for device >
sending 'boot' (3424 KB)...
OKAY [  0.364s]
writing 'boot'...
OKAY [  0.628s]
finished. total time: 0.992s
sending 'userdata' (26364 KB)...
OKAY [  2.816s]
writing 'userdata'...
OKAY [  4.909s]
finished. total time: 7.726s
sending 'system' (134304 KB)...
OKAY [ 14.387s]
writing 'system'...
OKAY [ 25.483s]
finished. total time: 39.870s
erasing 'cache'...
OKAY [  0.006s]
finished. total time: 0.006s
rebooting...

finished. total time: 0.001s
~~~

And there you go, a fresh FirefoxOS version.

Warning: __Flashing will WIPE ALL YOUR DATA!__

