Date: 2012-12-11
Title: Jackson + MongoDB's ObjectId
Tags: Java, Jackson
Category: Blog
Slug: jackson-mongodbs-objectid
Author: Eldelshell

This two classes should help you change the way Jackson serialization works 
for MongoDB's ObjectId. If you don't annotate your ObjectId fields 
with this classes, you should be receiving something like this:

~~~javascript
"id":{
  "new":false,
  "machine":-2068967138,
  "timeSecond":1355228408,
  "inc":175606344,
  "time":1355228408000
}
~~~

In my case, I needed my ObjectId's as:

~~~javascript
"id":"50c724f884ae111e0a778a48"
~~~

Well, here are the classes:

~~~java
public class ObjectIdSerializer extends JsonSerializer<ObjectId> {
    @Override
    public void serialize(
            ObjectId value,
            JsonGenerator jgen,
            SerializerProvider provider)
	throws IOException, JsonProcessingException
	{
        jgen.writeString(value.toHexString());
    }
}
~~~
 
~~~java
public class ObjectIdDeserializer extends JsonDeserializer<ObjectId>{
    @Override
    public ObjectId deserialize(
            JsonParser jp,
            DeserializationContext ctxt)
	throws IOException, JsonProcessingException
	{
        ObjectCodec oc = jp.getCodec();
        JsonNode node = oc.readTree(jp);
		// You could validate the input with ObjectId.valid(xxx)
        return new ObjectId(node.getTextValue());
    }
}
~~~
 
~~~java
@Document
public class MyDocument {
   
    @JsonDeserialize(using = ObjectIdDeserializer.class)
    @JsonSerialize(using = ObjectIdSerializer.class)
    private ObjectId id;
 
    private String name;
 
    ...
}
~~~
