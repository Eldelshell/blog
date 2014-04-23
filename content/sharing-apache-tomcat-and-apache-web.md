Date: 2014-04-20
Title: Sharing Apache Tomcat and Apache Web Server
Tags: Tomcat, HTTP
Category: Blog
Slug: sharing-apache-tomcat-and-apache-web 
Author: Eldelshell

Today's problem is sharing one single virtual host with different Tomcat instances. For example, say you have your Apache (the web server) with a virtual host for an intranet and you have in different Tomcat instances different applications like: monitoring, dashboard and hradmin. You want your users to be directed to the correct application if they access the URL _http://intranet/dashboard_ or _http://intranet/hradmin_.

In this example I'm using three Tomcat servers and this applications:

* server1:8080/monitoring/
* server1:8080/dashboard/
* hr1:8080/hradmin/
* hr2:8080/hradmin/

The __server1__ Tomcat is running two different applications and the _hr1_ and _hr2_ are running the _hradmin_ application which we want to be load balanced and since it's critical, to be always available.

The first thing to do is create the __jkworkers.properties__ file:

	# This names are the ones defined bellow
	worker.list=server1,hrlb
	worker.lock=P
	worker.status.type=status

	# Single server running monitoring and dashboard
	worker.server1.type=ajp13
	worker.server1.host=192.168.1.2
	worker.server1.port=8080
	worker.server1.disabled=false
	worker.server1.socket_timeout=60000
	worker.server1.connect_timeout=60000

	# Two workers for two servers running a critical application
	worker.hr1.type=ajp13
	worker.hr1.host=192.168.1.3
	worker.hr1.port=8080
	worker.hr1.disabled=false
	worker.hr1.socket_timeout=60000
	worker.hr1.connect_timeout=60000

	worker.hr2.type=ajp13
	worker.hr2.host=192.168.1.4
	worker.hr2.port=8080
	worker.hr2.disabled=false
	worker.hr2.socket_timeout=60000
	worker.hr2.connect_timeout=60000

	# Loadbalancer configuration for the critical application
	worker.hrlb.type=lb
	worker.hrlb.balance_workers=hr1,hr2
	worker.hrlb.sticky_session=true
	worker.hrlb.sticky_session_force=false
	worker.hrlb.method=R

Of course, you should use the DNS names instead of the IP addresses. Also, there are many more options to be set here, but this should give you a good start.

Second, you need your __jk.conf__ file:

~~~apache
JkWorkersFile /etc/apache2/conf.d/jkworkers.properties
JkLogFile /var/log/apache2/mod_jk.log
JkLogLevel info
JkLogStampFormat "[%a %b %d %H:%M:%S %Y]"
JkOptions +ForwardKeySize +ForwardURICompatUnparsed -ForwardDirectories
JkRequestLogFormat "%w %V %T"
JkShmFile /var/log/httpd/jk.shm
<Location /jkstatus>
	JkMount status
	Order deny,allow
	Deny from all
	Allow from 127.0.0.1
</Location>
~~~

And finally, you can set up your virtual host in the, for example, __intranet.conf__ file:

~~~apache
<VirtualHost *:80>
  ServerName intranet
  RewriteEngine on

  # Here we set where we want the url http://intranet/ to go
  RedirectMatch ^/$ /dashboard/

  DocumentRoot /srv/www/htdocs/docroot
  CustomLog  /var/log/apache2/access_reports combined
  ErrorLog  /var/log/apache2/error_reports
  
  # You can even setup a jongo proxy
  ProxyPass /jongo/ http://192.168.1.5:8080/jongo/
  ProxyPassReverse /jongo/ http://192.168.1.5:8080/jongo/
  
  # It's important that this names are the same used in your Tomcat
  JkMount /dashboard/* server1
  JkMount /monitoring/* server1
  JkMount /hradmin/* hrlb
</VirtualHost>
~~~

What we're doing here is telling the Apache server to listen on port 80 for all requests to the intranet host and to forward this requests to their corresponding applications:

* http://intranet/ goes to http://server1/dashboard/
* http://intranet/dashboard/ goes to http://server1/dashboard/
* http://intranet/monitoring/ goes to http://server1/monitoring/
* http://intranet/hradmin/ goes to http://hr1/hradmin/ or to http://hr2/hradmin/

Where you put this files depends on your httpd.conf configuration.

This example will allow a vanilla Apache HTTP server to serve three different applications (one load balanced) from three Tomcat servers (server1, hr1 and hr2)
