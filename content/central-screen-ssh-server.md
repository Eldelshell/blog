Date: 2011-01-20
Title: Central GNU Screen/SSH Server 
Tags: Linux, SSH, screen
Category: Blog
Slug: central-screen-ssh-server
Author: Eldelshell

I'm not going to explain why screen is such a great tool because it's and there are many blogs who will tell you so. What I'm going to explain is how you can use screen to setup a central server to manage and monitor who connects to your servers and what do they do.

Screen has the special ability that allows us to log and connect to running sessions. This becomes handy in our current objective: setting up a central server where all users must connect so they can connect to other servers.

The idea is pretty basic:

1. Fred connects to screen server (fred@screenserver)
2. Using the provided script, Fred connects to another server (ssh@anotherserver)

This has lots of advantages:

* No user management for each server
* Users know only one, easily changed password for all servers
* Greater control of user actions
* Monitor unscheduled access
* Log user activity

Of course, there are some disadvantages:

* Single point of failure
* Single point of entrance
* Can become a pain when transfering files

First, we need to setup a single server with the following:

1. SSH Client
2. GNU Screen
3. User account for each user (limit the user's group using quotas)
4. Common user account on each server you wish to connect to (i.e. foo)

You have your screen server, and on each server you have a user (i.e. ssh) with the same password (i.e. bar123) or using a certificate. Now secure you SSH configuration by allowing access only from the screen server to the _ssh_ user (and admin just in case):

	# /etc/hosts.allow
	sshd: 192.168.0.2/255.255.255.0
	sshd: 192.168.0.3/255.255.255.0
	# /etc/hosts.deny
	sshd: ALL
	# /etc/ssh/sshd_config
	AllowUsers ssh admin
	PermitRootLogin no

Your users should be able now to:

* Connect to the screen server using someuser@screenserver
* Connect to your servers only from the new screen server using foo@webserver

## Use some screen magic

If you include screen in this whole setup, you'll be able to log user activity in the servers by correctly configuring screen. First, add the following configuration to _/etc/screenrc_:

	# Scrolling
	defscrollback 1500
	termcapinfo xterm* ti@:te@

	# Detach on close
	autodetach on

	# Disable key binds
	bind H echo "Disabled" # Don't allow the user to disable logging
	bind d echo "Disabled" # Don't allow to detach
	bind ^d echo "Disabled" # Don't allow to detach
	bind c echo "Disabled" # Don't allow to create
	bind ^c echo "Disabled" # Don't allow to create
	bind S echo "Disabled" # Don't allow to split
	bind : echo "Disabled" # Don't allow to issue commands

	# no startup msg
	startup_message off

	# Logging
	deflog on
	logtstamp on
	logfile /tmp/screen-logs/%t-%Y%m%d-%n.log

On each user's home folder, create an empty _.screenrc_ file. This file should be owned by root with read only permits (since you don't want the users to modify it). This way, no user will be able to override the general configuration.

Next, and add your servers to this script:

```bash
#!/bin/bash
#
# Screener script
# version: 0.1
#

# Add your servers here
servers=(
    "foo@bar1"
    "foo@bar2"
    "foo@bar3"
)

server="${1}"

check_args (){
    local expected=1
    if [ $# -ne ${expected} ]; then
        echo "Usage ${0} server"
        exit 1
    fi
}

list_servers (){
    for i in ${servers[@]}; do
        echo "${i}"
    done
}

connect () {
    local username=$(whoami)
    local screen="/usr/bin/screen"
    local ssh="/usr/bin/ssh"
    local title="${username}.${server#*@}"
    local screen_opts="-S ${title} -t ${title}"
    local ssh_opts=""
    local connection="${ssh} ${ssh_opts} ${server}"
    ${screen} ${screen_opts} ${connection}
}

select_server (){
    echo "Select a server from the list. q to quit"
    list_servers
    read server
    if [ -z "${server}" ]; then
        select_server
    elif [ "${server}" == "q" ]; then
        echo "Quitting ${0}"
        exit 0
    fi
}

validate_server (){
    local exists=0
    for i in ${servers[@]}; do
        if [ "${server}" == "${i}" ]; then
            exists=1
        fi
    done
    if [ ${exists} -eq 0 ]; then
        echo "Unkown server ${server}"
        exit 1
    fi
}

if [ -z "${server}" ]; then
    select_server
fi

validate_server

echo "Connecting to ${server} $(whoami)"

connect 
```

This script allows a user to select a server from the given list and launchs a ssh session inside a screen session:

	/usr/bin/screen -S user.bar1 -t user.bar1 /usr/bin/ssh foo@bar1 

Since you're controlling and monitoring all the screen sessions, you can easily know what the users are doing on each server by watching the log files: user-20110116-0.log

Well, I hope this is useful for someone else. Leave a comment for any suggestions.
