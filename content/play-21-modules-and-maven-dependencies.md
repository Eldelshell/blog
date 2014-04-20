Date: 2013-02-11
Title: Play 2.1 Modules and Maven Dependencies
Tags: Play!, Maven
Category: Blog
Slug: play-21-modules-and-maven-dependencies
Author: Eldelshell

For a new project we've decided to use the new "modules" feature which Play 2.1 
brings to the framework. But, to be able to set our local maven repositories, 
it seems you have to do it for all sub-modules. So, in the parent's _Build.scala_
file you should use something like:

```scala
object ApplicationBuild extends Build {
 
  val appName         = "app"
  val appVersion      = "1.0-SNAPSHOT"
 
  val appDeps = Seq(
     javaCore,
     "groupId" % "app-core" % "0.1-SNAPSHOT"
  )
 
  val mainDeps = Seq(
     javaCore
  )
 
  // set all custom resolvers
  val myResolvers = Seq(
    "Local Maven Repository" at "file://"+Path.userHome.absolutePath+"/.m2/repository"
  )
 
  val common = play.Project(appName+"-common", appVersion,
      appDeps, path = file("modules/common")).settings(
        resolvers ++= myResolvers
      )
  val admin = play.Project(appName+"-admin", appVersion,
      appDeps, path = file("modules/admin")).dependsOn(common).settings(
        resolvers ++= myResolvers
      )
  val mobile = play.Project(appName+"-mobile", appVersion,
      appDeps, path = file("modules/mobile")).dependsOn(common).settings(
        resolvers ++= myResolvers
      )
 
  val main = play.Project(appName, appVersion, mainDeps).settings(
    resolvers ++= myResolvers,
    lessEntryPoints <<= baseDirectory(_ / "app" / "assets" / "css" ** "custom.less")
  ).dependsOn(admin, mobile).aggregate(admin, mobile)
}
```

With this you set all modules to use the same repositories, including the local maven repository.
