Date: 2013-07-29
Title: Font Awesome Icons in Android
Tags: android
Category: Blog
Slug: font-awesome-icons-in-android
Author: Eldelshell


Here's a small example of how to use Font Awesome in your Android apps. First of all, 
download font-awesome and place the __fontawesome-webfont.ttf__ file in your assets folder.
Then, add to your __strings.xml__ file the definitions generated like this:

```xml
<string name="icon_glass">&#xf000;</string>
<string name="icon_music">&#xf001;</string>
<string name="icon_search">&#xf002;</string>
<string name="icon_envelope_alt">&#xf003;</string>
<string name="icon_heart">&#xf004;</string>
```

To generate this XML you can use this small bash snippet:

```bash
grep "\f" variables.less | awk -F\" '{ print $1 $2 ";</string>" }' | sed 's/\\/\&#x/' | sed 's/@/<string name=\"icon_/' | sed 's/:\ /\">/' | sed 's/-/_/g'
```

Now, you'll need to set the _Typeface_ for each widget you're going to put an icon, for example, a __Button__:

```xml
<Button
 android:id="@+id/button2"
 android:layout_width="wrap_content"
 android:layout_height="wrap_content"
 android:textColor="#ff0000"
 android:text="@string/icon_heart" />
```

Then the Java code to use this Typeface looks like:

```java
Typeface font = Typeface.createFromAsset( activity.getAssets(), "fontawesome-webfont.ttf" );
...
button.setTypeface(font);

```

Since it's a font, you can control the color and size of the icons programmatically 
and the icons will scale automatically. The biggest downside is that 
the icons won't appear in the graphical layout.

![Android Button with FontAwesome Icon](|filename|/images/Selection_088.png "Android Button with FontAwesome Icon")

You can place your icons in pretty much any part of the __ActionBar__ title or in the tabs.

![Android Menu with FontAwesome Icons](|filename|/images/Selection_096.png "Android Menu with FontAwesome Icons")

```java
for (int i = 0; i < mSectionsPagerAdapter.getCount(); i++) {
    final TextView t = new TextView(this);
    t.setText(mSectionsPagerAdapter.getPageTitle(i));
    t.setTypeface(FONT_AWESOME);
    t.setTextColor(lightBlue);
    t.setTextSize(25);
    t.setPadding(0, 10, 0, 0);
    actionBar.addTab(actionBar.newTab().setCustomView(t).setTabListener(this));
}
 
// This goes into the FragmentPagerAdapter
@Override
public CharSequence getPageTitle(int position) {
    switch (position) {
        case 0:
            return activity.getResources().getString(R.string.icon_user);
```

You can also customize the __ActionBar__ title with a very cool hack. First,
you'll need to create a `MetricAffectingSpan` like this one:

```java
public class TypefaceSpan extends MetricAffectingSpan {
 
  private Typeface mTypeface;
  private float textSize;
  private int textColor;
 
  public TypefaceSpan(Context context, Typeface typeface, float textSize, int color) {
      this.textSize = textSize;
      this.textColor = color;
      this.mTypeface = typeface;
  }
 
  @Override
  public void updateMeasureState(TextPaint p) {
      p.setTypeface(mTypeface);
      p.setTextSize(textSize);
      p.setColor(textColor);
      p.setFlags(p.getFlags() | Paint.SUBPIXEL_TEXT_FLAG);
  }
 
  @Override
  public void updateDrawState(TextPaint p) {
      p.setTypeface(mTypeface);
      p.setTextSize(textSize);
      p.setColor(textColor);
      p.setFlags(p.getFlags() | Paint.SUBPIXEL_TEXT_FLAG);
  }
}
```

Then you change the __ActionBar__ title on your activity `onCreate` method:

```java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    SpannableString s = new SpannableString(iconMedic + " Activity");
    s.setSpan(
        new TypefaceSpan(this, FONT_AWESOME, 40, lightBlue),
        0,
        1,
        Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
    );

    // Update the action bar title with the TypefaceSpan instance
    ActionBar actionBar = getActionBar();
    actionBar.setTitle(s);
    actionBar.setIcon(android.R.color.transparent); // hide the app's icon
}
```

The result is the following:

![Android ActionBar with FontAwesome Icons](|filename|/images/Selection_095.png "Android ActionBar with FontAwesome Icons")

Well, that was some nice hacking with Android. Hope it's useful for you.

NOTE: I'm using FontAwesome 3.2.1 and Android 4.3 (API 18).
