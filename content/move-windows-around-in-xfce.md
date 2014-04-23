Date: 2012-08-16
Title: Move windows around in XFCE
Tags: XFCE, Python
Category: Blog
Slug: move-windows-around-in-xfce
Author: Eldelshell

There's this cool feature in Unity and MacOS (that I know of) where you can 
use some keybinding to place windows as blocks in your screen, like this:

![](|filename|/images/2_002.png)

The idea is that by pressing SUPER+LEFT the current window is placed on the left of your desktop.

![](|filename|/images/2_003.png)

As mentioned, XFCE doesn't support this out-of-the-box, but it's very easy to implement:

~~~python
#!/usr/bin/env python
# - coding: utf-8 -
 
import os, sys, subprocess, readline
from optparse import OptionParser
 
print_debug = True
xdotool_def_path = "/usr/bin/xdotool"
 
def debug(msg):
    if print_debug:
        print(msg)
 
def test_xdotool_installed():
    if not os.path.exists(xdotool_def_path):
        print("xdotool not installed. Quitting")
        sys.exit(1)
 
def get_desktop_dimensions(options):
    output = subprocess.check_output([xdotool_def_path, "getdisplaygeometry"])
    width, height = output.split(" ")
    width = int(width) - int(options.offset_x)
    height = int(height[:-1]) - int(options.offset_y) # trim last char which is \n
    return ( width, height )
 
def get_active_window():
    output = subprocess.check_output([xdotool_def_path, "getwindowfocus"])
    return output[:-1] # trim last char which is \n
 
def move_window(win_id, coords):
    debug("Moving Window %s to position %s, %s" % (win_id, coords[0], coords[1]))
    subprocess.call([xdotool_def_path, "windowmove", win_id, str(coords[0]), str(coords[1])])
 
def resize_window(win_id, dimension):
    debug("Resizing Window %s to dimension %s, %s" % (win_id, dimension.x, dimension.y ))
    subprocess.call([xdotool_def_path, "windowsize", win_id, str(dimension.x), str(dimension.y)])
 
class Dimension(object):
 
    def __init__(self, dim):
        self.x = dim[0]
        self.y = dim[1]
 
    def set_half_vertical_screen(self):
        self.x = self.x / 2
 
    def set_half_horizontal_screen(self):
        self.y = self.y / 2
 
    def set_section(self):
        self.x = self.x / 3
        self.y = self.y / 2
 
if __name__ == '__main__':
    test_xdotool_installed()
 
    parser = OptionParser(usage="You can combine options", version="0.1")
    parser.add_option("-l", "--left", action="store_true", dest="left", help="Move window to left half of screen")
    parser.add_option("-r", "--right", action="store_true", dest="right", help="Move window to right half of screen")
    parser.add_option("-u", "--up", action="store_true", dest="up", help="Move window to upper half of screen")
    parser.add_option("-d", "--down", action="store_true", dest="down", help="Move window to bottom half of screen")
    parser.add_option("-c", "--center", action="store_true", dest="center", help="Move window to center of screen")
    parser.add_option("", "--offset-x", dest="offset_x", default=0, help="Move window to center of screen")
    parser.add_option("", "--offset-y", dest="offset_y", default=0, help="Move window to center of screen")
    parser.add_option("-s", "--size", dest="size", help="Resizes the active window to the given size")
 
    (options, args) = parser.parse_args()
 
    desktop_dimensions = Dimension(get_desktop_dimensions(options))
    active_window_id = get_active_window()
 
    debug("Got dimension of desktop w:%s h:%s" % ( desktop_dimensions.x, desktop_dimensions.y))
    debug("Got window ID for active window %s" % active_window_id)
 
    if options.size:
        dim = Dimension(options.size.split("x"))
        resize_window(active_window_id, dim)
        sys.exit(0)
 
    coords = (0,0)
 
    if options.left:
        coords = (0,0)
        if options.up:
            desktop_dimensions.set_section()
 
        elif options.down:
            desktop_dimensions.set_section()
            coords = (0, desktop_dimensions.y)
           
        elif options.center:
            desktop_dimensions.set_section()
            coords = (0, desktop_dimensions.x / 3)
 
        else:
            desktop_dimensions.set_half_vertical_screen()
 
    elif options.right:
        coords = (desktop_dimensions.x / 2, 0)
        if options.up:
            desktop_dimensions.set_section()
            coords = (desktop_dimensions.x * 2, 0)
 
        elif options.down:
            desktop_dimensions.set_section()
            coords = (desktop_dimensions.x * 2, desktop_dimensions.y)
           
        elif options.center:
            desktop_dimensions.set_section()
            coords = (desktop_dimensions.x * 2, desktop_dimensions.y / 3)
 
        else:
            desktop_dimensions.set_half_vertical_screen()
 
    elif options.up:
        coords = (0,0)
        if options.center:
            desktop_dimensions.set_section()
            coords = (desktop_dimensions.x, 0)
        else:
            desktop_dimensions.set_half_horizontal_screen()
 
    elif options.down:
        coords = (0,desktop_dimensions.y / 2)
        if options.center:
            desktop_dimensions.set_section()
            coords = (desktop_dimensions.x, desktop_dimensions.y)
        else:
            desktop_dimensions.set_half_horizontal_screen()
 
    move_window(active_window_id, coords)
    resize_window(active_window_id, desktop_dimensions)
 
    sys.exit(0)
~~~

And that's pretty much it the whole script. You'll need to install _xdotool_ which 
is what does all the magic. 

To add your own shortcuts, got to `Settings -> Settings Manager -> Keyboard -> Application Shortcuts` and add your own.

![](|filename|/images/Keyboard_005.png)

As you can see in the screenshot, I saved this script as `/usr/bin/window-placer`

The options for the script are: 

*-u (up)
*-d (down)
*-l (left)
*-r right 

It also supports some combinations like -u -l (upper left corner) and so on. 
The --offset-y and --offset-x options are important if 
you don't want the window to hide the panels.
