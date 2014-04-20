Date: 2012-10-20
Title: Automate Play deployments with ANT and Jenkins
Tags: Java, Play!, Ant, Jenkins
Category: Blog
Slug: automate-play-deployments-with-ant-and-jenkins
Author: Eldelshell

Following my previous post A Play Framework server setup 
I'm going to write on how to automate the whole Play build-deploy cycle. 

In a nutcase, we have two servers (ci and play hosts), jenkins, an 
ANT script and a Bash script which will handle the servers restart in the host machines

Here's much of the ANT script in all its glory:

```xml
<property file="${user.home}/build.properties" />
<fail unless="play.path" message="Property play.path not set in build.properties file"/>
<fail unless="project.version" message="Property project.version not set"/>
<fail unless="project.path" message="Property project.path not set in build.properties file"/>
 
<property name="play.cache.repository" value="${play.path}/repository/cache/my.group.com" />
<property name="play.stage.dir" value="/target/staged" />
 
<tstamp/>
<property name="project.version.timestamp" value="${project.version}-${DSTAMP}${TSTAMP}"/>
 
<!-- On deploy we don't need to send all the files in the stage folder, but only the ones specific to our project -->
<patternset id="project.files.pattern">
    <include name="**/foo-*.jar"/>
    <include name="**/bar-*.jar"/>
    <include name="**/api-*.jar"/>
    <include name="**/joda-time*.jar"/>
</patternset>
 
<!-- This is what we'll call from Jenkins -->
<target name="jenkins-play-build" description="Specific target for jenkins">
   <antcall target="play-stage"/>
   <antcall target="deploy"/>
</target>
 
<target name="play-stage" description="Does a full build and stage of our Play apps">
    <!-- We have some maven projects which we want to update by deleting this folder-->
    <delete dir="${play.cache.repository}"/>
    <exec executable="${play.path}/play" dir="${my.repository.path}/foo">
      <arg value="clean"/>
      <arg value="compile"/>
      <arg value="stage"/>
    </exec>
    <exec executable="${play.path}/play" dir="${my.repository.path}/bar">
      <arg value="clean"/>
      <arg value="compile"/>
      <arg value="stage"/>
    </exec>
    <exec executable="${play.path}/play" dir="${my.repository.path}/api">
      <arg value="clean"/>
      <arg value="compile"/>
      <arg value="stage"/>
    </exec>
</target>
 
<target name="play-deploy" description="Deploys the given project">
    <fail unless="project.version.timestamp" message="Property version.timestamp needed to continue"/>
    <fail unless="deploy.server" message="Property needed to continue"/>
    <fail unless="webapp" message="Property webapp needed to continue"/>
    <property name="scp.path" value="${remote.user}@${remote.server}:${remote.dir}/webapps/${webapp}" />
    <sshexec
     host="${remote.server}"
     username="${remote.user}"
     keyfile="${user.home}/.ssh/id_rsa" trust="true"
     command="mkdir ${remote.dir}/webapps/${webapp}/${project.version.timestamp}" failonerror="false"/>
    <scp toDir="${scp.path}/${project.version.timestamp}" keyfile="${user.home}/.ssh/id_rsa" trust="true">
      <fileset dir="${project.path}/${webapp}/${play.stage.dir}" casesensitive="yes">
        <patternset refid="project.files.pattern"/>
      </fileset>
    </scp>
</target>
 
<!-- Deploy each of the projects separately. Repeat for each project. -->
<target name="play-deploy-foo" depends="check-play-foo-staged" if="project.foo.staged">
   <antcall target="play-deploy">
    <param name="webapp" value="foo"/>
   </antcall>
</target>
<target name="check-play-foo-staged">
      <echo message="Check path ${project.path}/foo$/{play.stage.dir} exists"/>
      <available file="${project.path}/foo/${play.stage.dir}" type="dir" property="project.foo.staged"/>
</target>
 
<!-- This is the target which binds everything together for the deploy -->
<target name="deploy" description="Deploy all applications">
   <antcall target="play-deploy-foo"/>
   <antcall target="play-deploy-api"/>
   <antcall target="play-deploy-bar"/>
   <sshexec
   host="${remote.server}"
   username="${remote.user}"
   keyfile="${user.home}/.ssh/id_rsa" trust="true"
   command="/home/play/bin/deploy ${project.version.timestamp}"/>
</target>
```

So, what we basically want here is to setup Jenkins to call a single ANT tasks, 
in this case _jenkins-play-build_ and set some properties as shown here:

![Jenkins](|filename|/images/Selection_006.png "Jenkins")

The script used to finish the deploy process will restart the Play apps 
and update the symlink pointing to the latest version we deployed

```bash
#!/bin/bash
#
# Script to automate CI deployments. Simply stop all
# servers, change the "current" symlinks to the given
# target folder and finally, start all servers
#
 
play_home="/home/play"
webapps_folder="${play_home}/webapps"
export JAVA_HOME="/usr/lib/jvm/default-java"
 
apps=( "bar" "api" "foo" )
 
for app in ${apps[@]}; do
 
    echo "Stopping server ${app}"
    ${play_home}/bin/${app} stop
 
    echo "Regenerate current symlink of ${app}"
    rm ${webapps_folder}/${app}/current
    ln -s ${webapps_folder}/${app}/${1} ${webapps_folder}/${app}/current
 
    echo "Starting server ${app}"
    ${play_home}/bin/${app} nohup
 
done
 
exit 0
```
For this to work, you'll need to configure SSH password-less authentication between you CI server and the target servers.
