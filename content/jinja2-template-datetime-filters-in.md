Date: 2013-03-14
Title: Jinja2 template datetime filters in Flask
Tags: jinja2, flask
Category: Blog
Slug: jinja2-template-datetime-filters-in
Author: Eldelshell


Well, I'm really liking Flask for the moment. It's light, convenient and well 
documented. Also, Jinja2 is quite powerful and things are building up pretty fast.

A filter alters a variable in a template. It's mostly for formatting purpose. 
In the template, it's separated from the variable by a pipe character (|). See 
[Template Designer Documentation](http://jinja.pocoo.org/docs/templates/#filters) 
for details. There's a bunch of builtin filters, 
covering a wide range of cases. But sometimes, you may need more. Fortunately, 
it's pretty easy to add new Jinja2 filters in Flask.


In our task at hand, we don't have a filter to localize dates, so let's build one.

In Jinja2 a filter is a block of code that is applied on user demand on a given variable in a template.

First, you need to have Flask-Babel up and running. Next we will create our filter:

~~~python
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

import datetime
from flask.ext.babel import gettext

@app.template_filter('date')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime(gettext('%%m/%%d/%%Y'))
~~~

On your Jinja2 templates, you only need a datetime and apply the date filter:

~~~python
{{ obj.date | date }}
~~~

Or pass it a different format

~~~python
{{ obj.date | date(_('%%Y.%%m.%%d')) }}
~~~

The only "magical" parts here is the `gettext('%%m/%%d/%%Y')` and `_('%%Y.%%m.%%d')`. 
Now you can add to your different .po files the different formats to use for each language.
