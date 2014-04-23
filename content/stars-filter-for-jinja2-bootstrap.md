Date: 2013-04-01
Title: Stars filter for Jinja2 + Bootstrap
Tags: bootstrap, jinja2, flask
Category: Blog
Slug: stars-filter-for-jinja2-bootstrap
Author: Eldelshell

Here's a simple Jinja2 filter to add FontAwesome 3.2.1 stars to a template:

~~~python
@app.template_filter('stars')
    def _jinja2_filter_stars(value):
        """
        Adds filled and empty stars
        Usage: {{ obj.stars|stars|safe }}
        """
        ret = ""
        if value:
            for i in range(1, value+1):
                ret += '<i class="icon-star"></i>'

            for i in range(value, 5):
                ret += '<i class="icon-star-empty"></i>'
        return ret
~~~

