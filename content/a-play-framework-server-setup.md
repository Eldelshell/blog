Date: 2012-09-08
Title: A Play Framework server setup
Tags: Java, Play!
Category: Blog
Slug: a-play-framework-server-setup
Author: Eldelshell

What a wonderful surprise was that Play 2.0.x can't be deployed to 
application servers. Yes, there's a [plugin](https://github.com/dlecan/play2-war-plugin), but I'm not really fond 
on depending in some guy's project for my business critical applications 
and the generated WAR wasn't really helpful since you still need to 
run a different instance of your application server for each Play 
application because you can only deploy to root ("/") and not as a specific path ("/myapp/").

Netty, although I don't get the whole .io domains thing, is what the 
guys at Play decided to use, so, for those of you who use Apache HTTP 
you can drop the AJP plugin and install the proxy_mod and proxy_http_mod.

When setting up a server, be it Tomcat, JBoss or Glassfish, my main 
target is flexibility and ease of configuration. I hate having to 
modify 30 different logger.xml files because some guy doesn't know 
about symlinks, or having to perform 30 manual operations to 
perform a release. Also, the start/stop process has to be as easy 
and centralized as possible since you never know who is the guy 
restarting your cluster at 4:00am is. Finally, deployments 
have to be as light and fast as possible.

With those objectives in mind, this is what I came up with:

~~~bash
$tree /home/play
|-- bin
| |-- all        #(script to start/stop all applications)
| |-- play       #(script to start/stop the foo applications)
| |-- deploy     #(script to deploy the applicationa)
|-- etc
| |-- application.conf #(common Play configuration file used by all applications)
| `-- logger.xml       #(common Logger configuration file used by all apps)
|-- lib
|   |-- 2.0.2 
|   |    |-- akka-actor.jar
|   |    |-- akka-slf4j.jar
|   |    |-- ...
|   |    `-- xml-apis.jar
|   |-- 2.0.3
|   |    |-- akka-actor.jar
|   |    |-- akka-slf4j.jar
|   |    |-- ...
|   |    `-- xml-apis.jar|   
    `-- play -> lib
|-- logs #(Folder for log files from the different applications)
|   |-- foo.log
|   |-- bar.log
|   `-- api.log
`-- webapps #(Folder which contains our applications)
    |-- bar    
    | |-- 0.1-SNAPSHOT    
    | | |-- joda-time-2.1.jar    
    | | |-- foo_2.9.1-1.0-SNAPSHOT.jar    
    | | |-- foo-common-0.1-SNAPSHOT.jar
    | `-- current -> 0.1-SNAPSHOT
    |-- api    
    | |-- 0.1-SNAPSHOT
    | | |-- joda-time-2.1.jar    
    | | |-- foo-api_2.9.1-1.0-SNAPSHOT.jar    
    | | |-- foo-common-0.1-SNAPSHOT.jar
    | `-- current -> 0.1-SNAPSHOT    
    `-- foo      
      |-- 0.1-SNAPSHOT
      | |-- joda-time-2.1.jar      
      | |-- foo-common-0.1-SNAPSHOT.jar      
      | |-- foo-bar_2.9.1-1.0-SNAPSHOT.jar
      `-- current -> 0.1-SNAPSHOT
~~~

There are two tricky parts here: creating the startup scripts with the correct classpath 
and separating Play's jar files from yours. Since my projects dependencies were few 
it was easy to simply copy them over from the target/stage folder. Another solution 
is to generate an empty Play application, run the stage option and copy the files generated there.

The startup scripts, however you do them, you have to provide the correct options to Java:

~~~bash
#!/bin/bash
#
# Play Admin Script
# This script is to be used to handle operations with our Play
# servers. This script is able to start, stop, and report on the
# status of our servers
#
 
play_home="/home/play"
app_id="my-play-app"
app_port="9000"
out_file="${play_home}/logs/${app_id}/${app_id}.out"
 
do_start () {
    local app_path="${play_home}/webapps/${app_id}"
    local config_file="${play_home}/etc/application.conf"
    local logger_file="${play_home}/etc/logger.xml"
    local path="${play_home}/lib/play/*:${app_path}/current/*"
    local opts="-Dapp.id=${app_id} -Dhttp.port=${app_port} -Xms128m -Xmx512m -server -XX:MaxPermSize=128m -Dconfig.file=${config_file} -Dlogger.file=${logger_file}"
 
    local exit_code=10
    while [ $exit_code -eq 10 ]; do
        "${JAVA_HOME}/bin/java" ${opts} -cp "${path}" play.core.server.NettyServer "${app_path}"
        exit_code=$?
    done
}
 
do_stop () {
    pkill -f "app.id=${app_id}"
    exit $?
}
 
do_status () {
    pkill -0 -f "app.id=${app_id}" > /dev/null 2>&1 && echo "Process is running" && exit 0
    echo "Process is not running" && exit 0
}
 
### main ###
 
if [ "$(whoami)" != "play" ]; then
   echo "This script must be run as ubuntu user" 1>&2
   exit 1
fi
 
if [ "${JAVA_HOME}" == "" ]; then
    echo "JAVA_HOME Not set. Install the JRE and set the JAVA_HOME in your initialization file"
    exit 1
fi
 
if [ ! -d "${JAVA_HOME}" ] ; then
    echo "Java ${JAVA_HOME} Directory doesn't exist."
    exit 1
else
    if [ ! -x "${JAVA_HOME}/bin/java" ] ; then
        echo "Java binary error: not found or not executable"
        exit 1
    fi
fi
 
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
        nohup $0 $1 start > "${out_file}" 2>&1 &
    ;;
 
    *)
        echo "Usage: $0 start|nohup|stop|status"
        exit 1
    ;;
esac
 
exit 0
~~~

This will work with JDK 6 and JDK 7 which are the only ones which support this 
classpath definitions. Since we're running many Play instances, we need to 
provide different ports with the http.port options. To configure Play to 
use our common application.conf (which holds the configuration for the 
database connection) we use the _config.file_ options. Finally, to provide different 
logger configurations to Logback we use the logger.file option.

What is accomplished by this setup:

* Very Unix like structure (bin, logs, etc)
* Easy deploy (simply replace the current symlink)
* Easy patching (replace one of your jars and restart)
* Easy servers control (bash scripts)


