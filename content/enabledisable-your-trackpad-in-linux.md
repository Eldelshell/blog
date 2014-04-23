Date: 2012-07-26
Title: Enable/Disable your Trackpad in Linux
Tags: Linux, Hack
Category: Blog
Slug: enabledisable-your-trackpad-in-linux
Author: Eldelshell

Here's a small post about enabling/disabling a your trackpad, touchpad, or whatever you want to call it in Linux.

First, get to know your stuff with:

~~~bash
$ xinput --list
⎡ Virtual core pointer                     id=2 [master pointer  (3)]
⎜   ↳ Virtual core XTEST pointer               id=4 [slave  pointer  (2)]
⎜   ↳ DualPoint Stick                          id=13 [slave  pointer  (2)]
⎜   ↳ Logitech Optical USB Mouse               id=11 [slave  pointer  (2)]
⎜   ↳ AlpsPS/2 ALPS DualPoint TouchPad         id=14 [slave  pointer  (2)]
⎣ Virtual core keyboard                    id=3 [master keyboard (2)]
↳ Virtual core XTEST keyboard              id=5 [slave  keyboard (3)]
↳ Power Button                             id=6 [slave  keyboard (3)]
↳ Video Bus                                id=7 [slave  keyboard (3)]
↳ Power Button                             id=8 [slave  keyboard (3)]
↳ Sleep Button                             id=9 [slave  keyboard (3)]
↳ Laptop_Integrated_Webcam_3M              id=10 [slave  keyboard (3)]
↳ AT Translated Set 2 keyboard             id=12 [slave  keyboard (3)]
↳ Dell WMI hotkeys                         id=15 [slave  keyboard (3)]
~~~

This is what my current laptop (Dell M4500) shows. In this case we have three mice devices in the laptop: DualPoint Stick and AlpsPS/2 ALPS DualPoint TouchPad are in the laptop itself, and attached is the Logitech Optical USB Mouse.

Now I want to disable those two devices and leave the Logitech mouse only. To do this simply run the following:

~~~bash
$xinput --set-prop "AlpsPS/2 ALPS DualPoint TouchPad" "Device Enabled" 0
$xinput --set-prop "DualPoint Stick" "Device Enabled" 0
~~~

You also might want to add a few lines to your _.bashrc_ like:

~~~bash
function enable-trackpad(){
	xinput --set-prop "AlpsPS/2 ALPS DualPoint TouchPad" "Device Enabled" 1
	xinput --set-prop "DualPoint Stick" "Device Enabled" 1
}
function disable-trackpad(){
	xinput --set-prop "AlpsPS/2 ALPS DualPoint TouchPad" "Device Enabled" 0
	xinput --set-prop "DualPoint Stick" "Device Enabled" 0
}
~~~

Hope this helps
