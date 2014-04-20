Date: 2013-03-04
Title: Play + Bootstrap + Dates
Tags: Play!
Category: Blog
Slug: play-bootstrap-dates
Author: Eldelshell


First of all, I hate HTML date input fields, because they're so broken when you start 
playing with different formats for different locales, and HTML5 `input=date` doesn't 
help either since not all browsers implement this and in case of Google's Chrome, 
it's so ugly that you won't use it.

To try to cope with this I'm using this date picker for Bootstrap which handles 
things pretty well until you hit a wall with how Play handles form data for dates. 
Basically, the problem is that even if your form class has a Date field and 
you registered a custom formatter as [explained here](http://stackoverflow.com/questions/13709987/play-2-0-framework-custom-form-field/13842675#13842675)
, the Date value is not formatted when the template is rendered. Some code to explain

```java
public class MyForm {
    public LocalDate myDate;
}
```

In the controller you would have something like:

```java
MyForm myForm = new MyForm();
myForm.myDate = new LocalDate();
return ok(
	views.html.somePage.render(
		form(MyForm.class).fill(myForm)
	)
);
```

If you try to use the value from this form you'll see that it follows the ISO 
format yyyy-MM-dd, which is fine, until you're asked for this field to follow 
specific locale formats like dd/mm/yyyy or mm/dd/yyyy.

To fix this I've created my own implementation of the inputDate template:

```html
@(field: play.api.data.Field, args: (Symbol,Any)*)(implicit handler: helper.FieldConstructor, lang: play.api.i18n.Lang)
 
@**
 * A reimplementation of the default inputDate.
 * Example:
 * {{{
 * @import views.html.forms.inputDate
 * @import play.data.format.Formatters
 * ...
 * @inputDate(
 *    myForm("myDate"),
 *    '_label -> Messages("label.myDate"),
 *    'class -> "date-picker",
 *    'dateValue -> Formatters.print(myForm.get().start),
 *    'dateFormat -> Messages("date.format")
 * )
 * }}}
 *
 * In your JS code (as explained here http://www.eyecon.ro/bootstrap-datepicker/):
 * $('.date-picker').datepicker();
 *
 *@
 
@import play.api.i18n._
@import views.html.helper._
 
@inputType = @{ args.toMap.get('type).map(_.toString).getOrElse("text") }
@dateFormat = @{ args.toMap.get('dateFormat).map(_.toString).getOrElse("yyyy-mm-dd") }
@dateValue = @{ args.toMap.get('dateValue).map(_.toString).getOrElse(field.value) }
 
@input(field, args:_*) { (id, name, value, htmlArgs) =>
    <input 
		type="@inputType"
		id="@id" name="@name"
		value="@dateValue"
		data-date-format="@dateFormat" 
		@toHtmlArgs(htmlArgs) >
}
```



