Date: 2012-12-13
Title: Play! 2.1-RC1 Migration mini-guide
Tags: Play!, Java
Category: Blog
Slug: play-21-rc1-migration-mini-guide
Author: Eldelshell

Tonight I took up to the task of migrating an app from Play! 2.0.3 to 2.1-RC1 
to checkout what's new. First of all, what you will need to change to simply 
be able to boot up the play console without an `org.scala-sbt#sbt;0.11.3: not found` error being raised.

In the file plugins.sbt you need to change the line:

```scala
addSbtPlugin("play" % "sbt-plugin" % "2.0.3")
addSbtPlugin("play" % "sbt-plugin" % "2.1-RC1")
```

In the file _build.properties_ you need to change:

```
sbt.version=0.11.3
sbt.version=0.12.0
```
Finally, the file _Build.scala_ should look like:

```scala
import sbt._
import Keys._
// 2.0.3 import PlayProject._
import play.Project._
 
object ApplicationBuild extends Build {
 
    val appName         = "test"
    val appVersion      = "1.0-SNAPSHOT"
 
    val appDependencies = Seq(
        javaCore, javaJdbc, javaEbean,
        // more dependencies
        "com.yahoo.platform.yui" % "yuicompressor" % "2.4.7"
    )
 
    // 2.0.3 val main = PlayProject(appName, appVersion, appDependencies, mainLang = JAVA).settings(
    val main = play.Project(appName, appVersion, appDependencies).settings(
        resolvers += "Local Maven Repository" at "file:///"+Path.userHome.absolutePath+"/.m2/repository/"
    )
}
```

Now you should be able to run play on your project and start changing 
stuff... since there are more changes which once you "run" or  "compile" 
you'll find out. For example, if you ever used `form(Entity.class)` now 
you'll need to import form as `import static play.data.Form.form`.
