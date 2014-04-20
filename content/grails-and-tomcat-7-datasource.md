Date: 2011-09-12
Title: Grails and Tomcat 7 Datasource
Tags: Grails, Tomcat
Category: Blog
Slug: grails-and-tomcat-7-datasource
Author: Eldelshell

This should be fast and easy. You want a shared datasource on your Tomcat 7 server, which you can change without deploying a new Grails war and that is shared between all your Grails applications on this same Tomcat server.

You have to configure your __DataSource.groovy__ file with this:

	production{
		pooled = false
		dbCreate = "update"
		jndiName = "java:comp/env/jdbc/MyGrailsDS"
	}

Generate your war, place it for deployment and go configure the `conf/context.xml` file on your Tomcat server.

	<Resource 
		name="jdbc/MyGrailsDS" 
		auth="Container" 
		type="javax.sql.DataSource" 
		username="abc" 
		password="abc" 
		driverClassName="com.mysql.jdbc.Driver" 
		url="jdbc:mysql://localhost:3306/my_grails_schema"/>

Start your Tomcat 7 server and enjoy. Now you can change the database your applications point at by simply changing the configuration on the `context.xml` file.
