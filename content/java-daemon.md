Date: 2011-04-13
Title: Java Daemon
Tags: Java, Bash
Category: Blog
Slug: java-daemon
Author: Eldelshell

Here's a little Bash script to run any Java application as a daemon. The only change you'll have to implement in your Java application is a handler for UNIX kill signals. Something like this:

```java
Signal.handle(new Signal("INT"), new SignalHandler () {
	public void handle(Signal sig) {
		System.exit(10);
	}
});
```

That's an example, handle exceptions and other signals properly.

Now that your application is ready to handle a signal, be sure to be very special with the signal 10 and exit with code 10. Why 10? Read the kill manual page and you'll see there are no standard signals with this value.

Here's the Bash code:

```bash
#!/bin/bash
#
# Startup Script

JAVA_HOME="/opt/jre1.6.0_18/"
runnable="com.test.TestApplication"
pid=""

do_start () {
    if [ ! -d "${JAVA_HOME}" ] ; then
        echo "${JAVA_HOME} Directory doesn't exist."
        exit 1
    else
        if [ ! -x "${JAVA_HOME}/bin/java" ] ; then
            echo "Java binary error: not found or not executable"
            exit 1
        fi
    fi

    local path="lib/*"
    local opts="-Ddebug.level=INFO"

    # Launch the process
    local exit_code=10
    while [ $exit_code -eq 10 ]; do
        "${JAVA_HOME}/bin/java" ${opts} -cp "${path}" ${runnable}
        exit_code=$?
    done
}

do_stop () {
    getPID 
    kill ${pid} > /dev/null 2>&1 && echo "Stoping process ${pid}"
}

do_status () {
    getPID 
    kill -0 ${pid} > /dev/null 2>&1 && echo "Process is running"
}

do_restart () {
    getPID 
    kill -10 ${pid}  > /dev/null 2>&1 && echo "Restarting"
}

getPID () {
    # not the best, but works on most linuxes
    pid=$( ps -ef | grep  ${runnable} | grep -v grep | awk '{ print $2 }' )
}

case ${1} in
    start)
        do_start
    ;;

    stop)
        do_stop
    ;;

    status)
        do_status
    ;;

    nohup)
        # I really like this hack 
        nohup $0 start > /dev/null 2>&1 &
    ;;
    
    restart)
        do_restart
    ;;

    *)
        echo "Usage: $0 start|nohup|restart|stop|status"
        exit 1
    ;;
esac

exit 0
```

I believe the script is pretty straight forward. Cool thing is that if you use start, you will run your application normally, but using the nohup option, it will call nohup on the script and run itself in daemon mode. Now, the only way to stop this process is to call the stop option or directly kill it. Also, if your process somehow listens for any event, you can implement a special one which allows the process to restart itself. For example, if your application is a web service, you can call `curl http://localhost/restart`

