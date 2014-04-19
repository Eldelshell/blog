Date: 2013-04-23
Title: A (Simple) Big Data Architecture
Tags: big-data, architecture
Category: Blog
Slug: a-simple-big-data-architecture
Author: Eldelshell

How does a Big Data architecture looks like?

![Big Data Architecture](|filename|/images/bigdata.png "Big Data Architecture")

Of course, your requirements/tools surely can change, but this should give you a pretty good 
abstract view of the different layers applied in a Big Data environment. There are many 
things missing, like caching (memcached), data indexing (Solr), task execution (Zookeeper) and 
data extraction/analysis/mining software (there are so many).

You might choose not use a different NoSQL solution but directly use HBase for your NoSQL 
data or use different NoSQL software for different data (HBase & Neo4J).
