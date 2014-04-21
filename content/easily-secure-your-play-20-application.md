Date: 2012-08-12
Title: Easily Secure your Play 2.0 Application
Tags: Java, Play!
Category: Blog
Slug: easily-secure-your-play-20-application
Author: Eldelshell

This is my first post about Play Framework. It's quite an interesting 
framework because of its dissociative identity disorder between 
Java and Scala. I'm liking it actually, except for two key things:

* The name (it's impossible to search stuff on the Net) 
* The documentation (which brings us to this post) 
* No IDE support for the Scala HTML stuff (at least in Eclipse Juno) 

Nevertheless, it has some interesting stuff built in it like its MVC model 
based on annotations, the routes file, database evolution and those 
good looking TODO and error pages.

## Authentication on Play!

After having some forms ready I got to the point of authentication, and 
lucky me (and for this blog) there's nothing, nada, niet, in Play's documentation 
about this. But, when you download Play 2.0.x you get a folder with 
samples for Java and Scala which I recommend because it's very useful. In 
this case the __Zentasks__ project has a good starting point for 
understanding authentication in Play.

You can start with the plain application generated by play, run it and 
test that you get that nice welcome page that Play generates.

Then generate these files:

* Secured.java (auth) 
* User.java (model) 
* Authentication.java (controller) 
* LoginForm.java (view) 

Here's all the code:

	@Entity
	@Table(name="user")
	public class User {
	 
	  @Id
	  @GeneratedValue
	  public Long id;
	 
	  public String email;
	  public String password;
	 
	}
	 
	public class LoginForm {
	 
	  @Required
	  @Constraints.Email
	  private String email;
	 
	  @Required
	  @Constraints.MinLength(value=4)
	  private String password;
	 
	 
	  public String validate() {
		if(Authentication.authenticate(this.email, this.password) == null) {
		  return "Invalid user or password";
		}
		return null;
	}
	 
	public final class Authentication extends Controller {
	 
		public static Result login() {
			return ok(
				login.render(form(LoginForm.class))
			);
		}
	   
		public static Result authenticate() {
		 // the validate method of the form has already been called
			Form<LoginForm> loginForm = form(LoginForm.class).bindFromRequest();
			if(loginForm.hasErrors()) {
				return badRequest(login.render(loginForm));
			} else {
				session("email", loginForm.get().getEmail());
				return redirect(
					routes.Application.index()
				);
			}
		}
	   
		public static User authenticate(final String email, final String password){
		 return Ebean.find(User.class)
		 .where()
		 .eq("email", email)
			.eq("password", Base64.getSHABase64(password))
			.findUnique();
		}
	 
	 
		public static Result logout() {
			session().clear();
			flash("success", "You've been logged out");
			return redirect(
				routes.Authentication.login()
			);
		}
	 
	}
	 
	public class Secured extends Security.Authenticator {
	   
		@Override
		public String getUsername(Context ctx) {
			return ctx.session().get("email");
		}
	   
		@Override
		public Result onUnauthorized(Context ctx) {
			return redirect(routes.Authentication.login());
		}
	}
	 
	@Security.Authenticated(Secured.class)
	public class Application extends Controller {
	  public static Result index() {
		Logger.debug("Logged in as user " + Context.current().request().username());
		return ok(index.render("Your new application is ready."));
	  }
	}

The `User` model (1-12) will be responsible of persisting our authentication 
data (email, password, etc) and it's a standard JPA annotated class

Note here that we are not extending from `play.db.ebean.Model` nor we are 
using Play constraint annotations because in this example I wanted to also 
show that it's possible to use standard JPA entities. This means that our 
models can live outside of Play in a separate JAR with no dependencies 
to any ORM so we can reuse our models from different applications 
with different ORMs (at the moment I was testing with using 
Ebean or Hibernate for our project) or even with plain JDBC.

The `LoginForm` (14-30) class is bind to our form in the `login.scala.html` view:

	@(form: Form[com.play.forms.LoginForm])
 
	<html>
	 <head>
	  <title>Please Login</title>
	 </head>
	 <body>
		   
	  @helper.form(routes.Authentication.authenticate) {
			   
		<h1>Sign in</h1>
			   
		@if(form.hasGlobalErrors) {
		  <p class="error">
		   @form.globalError.message
		  </p>
		}
			   
		<p>
		 <input type="email" name="email" placeholder="Email" value="@form("email").value">
		</p>
		<p>
		 <input type="password" name="password" placeholder="Password">
		</p>
		<p>
		 <button type="submit">Login</button>
		</p>
			   
	 }
	 </body>
	</html>

The validate() method (25) is important because Play uses 
[Spring to validate the forms data](http://www.playframework.org/documentation/2.0.2/JavaForms). 
In this case the validation is being done by Play's Constraints annotations and we use the method to authenticate the user.

You could also implement the `org.springframework.validation.Validator` interface if that makes you feel more confident.

The `login.scala.html` is a simple HTML form with the binding to the `LoginForm` (full package name)

The `Authentication` controller (32-70) is the responsible of handling the actions 
associated to authentication: login (34) and logout (62); and provides the authentication method (53).

The `Secured` class (72-83) will handle authentication specific logic, like what to do with unauthenticated users.

This class is a good place to add groups or profiles specific methods like isOwner or isMember.

We then need to annotate the controllers we want to be protected and since we're starting 
with the bootstrapped application, we will secure the `Application` controller with the 
annotation `@Security.Authenticated(Secured.class)` (line: 85)

And finally, edit your routes file to reflect the new controller

	# Home page
	GET /        controllers.Application.index()

	# Authentication
	GET  /login  controllers.Authentication.login()
	POST /login  controllers.Authentication.authenticate()
	GET  /logout controllers.Authentication.logout()

Oh! And of course you have to configure your datasource to use the H2 database. Now 
restart the whole thing and when you go to _http://localhost:9000/_ you'll be 
redirected to _http://localhost:9000/login_ and to logoff go to _http://localhost:9000/logout_

## Common Models

One final note on having the models in a different JAR. For this example I created 
a maven project called __common-models__ where all the persistence models and 
their tests are contained separately from the main Play application. To be able 
to add this project as a dependency to play, the __Build.scala__ file should have something like:

	val appDependencies = Seq(
	  "com.play" % "common-models" % "0.1-SNAPSHOT",
	)
	val main = PlayProject(appName, appVersion, appDependencies, mainLang = JAVA).settings(
	  resolvers += "Local Maven Repository" at "file:///"+Path.userHome.absolutePath+"/.m2/repository/"
	)

And your _application.conf_ ORM configuration should have something like:

	db.default.driver=org.h2.Driver
	db.default.url="jdbc:h2:mem:play"
	db.default.user=sa
	db.default.password=''
	ebean.default="com.play.models.*"

In the _common-models_ project I have the structure of the models as:

	com.play.models.AbstractEntity
	com.play.models.auth.User
	com.play.models.auth.Profile
	com.play.models.store.Location
	com.play.models.store.Store

Just so you get the idea.