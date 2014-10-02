Date: 2014-10-02
Title: What is Docker
Tags: docker
Category: Blog
Slug: whats-docker
Author: Eldelshell


According to [docker.io][1] Docker is:

> an open platform for developers and sysadmins to build, ship, and run distributed applications.

In case that doesn't make any sense let me explain with a simple example.

Before Docker, if you wanted to do some development with a RDBMS like MySQL you would install it in your
computer or in a development server. The same for every other technology you might use:

* memcached
* web server
* application server

The process would be like:

* Install & configure MySQL
* Install & configure memcached
* Install & configure web server
* Install & configure application server
* Install & configure development environment

If you don't see the pain in this is because you haven't spent two days setting up a development environment. Some tools
like Puppet or Chef automate this process with a script or DSL solution. Docker takes this a little further and also isolates
all of this in one or several virtual machines (containers) separate of the host operating system. Actually, Chef or Puppet and
Docker work really nice together if you have to create complex images.

With Docker, you would simply do something like:

```sh
$ docker run --name my-dev-environment -d -P -e MYSQL_ROOT_PASSWORD=1234 company-dev-image
```

This would download, install and configure all that stuff and place it in a virtual machine like:

```sh
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
postgres            9.3.5               75af0ca1d93c        13 hours ago        213.1 MB
postgres            latest              75af0ca1d93c        13 hours ago        213.1 MB
postgres            9.3                 75af0ca1d93c        13 hours ago        213.1 MB
mysql               latest              722147135e89        13 hours ago        235.6 MB
company-dev-image   latest              d7734f8df1fc        13 hours ago        765.3 MB
```

All of this would be running in a virtual machine which you can stop, modify and distribute
to your peers in case a modification is made.

## Concepts

There are three basic concept you need to know when working with Docker:

### Registry

This is where all Docker _images_ are stored. There's the [central Docker registry][2] and then
you can create your own registry server. To access this registry server:

```sh
$ docker login http://mycompany.registry.server
```

You can search the registry servers you're signed to for different images with:

```sh
$ docker search postgres
NAME                     DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
postgres                 PostgreSQL is a powerful, open source obje...   218       [OK]       
paintedfox/postgresql    A docker image for running Postgresql.          43                   [OK]
helmi03/docker-postgis   PostGIS 2.1 in PostgreSQL 9.3                   18                   [OK]
```

### Images

A Docker image is the mean of distribution of a set of components. Images are defined by a `Dockerfile` which
describes this components and their behavior. For example, check the [MySQL server Dockerfile][3]. Docker images
are similar to other Virtual Machine software images like VirtualBox or QEMU.

To checkout the images you have in your system, type `docker images`.

You can add images with `docker run` or with `docker pull`. Here are some examples using images:

```sh
$ docker run --name my-super-cool-postgres -d postgres
```

Will download the default image from the _postgres_ repository and create/run a new container with the name _my-super-cool-postgres_.

```sh
$ docker pull postgres       // Download all images in the postgres repository
$ docker pull postgres:9.4   // Download only the image tagged 9.4

$ docker rmi postgres        // Deletes all images of postgres repository
$ docker rmi postgres:9.4    // Deletes only the image for 9.4
```

The `pull` command won't create any container.

### Containers

A container is an instance of an image being executed. You can have several containers of the same image running at the same
time. To checkout all the containers run:

```sh
$ docker ps -a
CONTAINER ID        IMAGE               STATUS                         PORTS               NAMES
251eee778c08        mysql:latest        Up About an hour               3306/tcp            jongo-mysql         
80ddbb08a173        postgres:9          Exited (0) About an hour ago                       jongo-pg
```

Here you can see all the containers, their state, name and ports. You also perform several operations with the containers:

```sh
$ docker stop my-super-cool-postgres // stop this container
$ docker rm my-super-cool-postgres   // delete this container
```

Containers can communicate between them with the `--link` option. You can create temporary containers with the `--rm` option and
you can open a port in your host machine to the container with the `-P & -p` options.

This is has been my introduction to Docker and only the future will tell where this technology takes us, but as I see it, the biggest
issue Docker will help is with the "it works in my machine" syndrome and ease the whole release process. For example, I can see a full
continuous integration and delivery process that tests, builds, packages and releases a Docker container from the moment a developer
pushes to a branch. And yes, many places are starting to use Docker in production.


  [1]: http://docker.io
  [2]: https://registry.hub.docker.com/
  [3]: https://github.com/docker-library/mysql/blob/7461a52b43f06839a4d8723ae8841f4cb616b3d0/5.6/Dockerfile
