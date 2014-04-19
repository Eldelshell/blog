Date: 2013-05-28
Title: A jQuery Mobile Progress Bar
Tags: jquery-mobile
Category: Blog
Slug: a-jquery-mobile-progress-bar
Author: Eldelshell

Been working on different apps for FirefoxOS, which I'm loving by the way.

For my latest app I've been using jQuery Mobile which, to my surprise, doesn't come with a progress bar control.

Luckily for you, here's the code to generate yours with as few lines of code as possible.

```html
<html>
<head>
    <style type="text/css">
        .progress-bar input[type=number], .ui-slider-handle {
            display: none;
        }  
        .progress-bar .ui-slider-track {
            margin: 0px;
        }
    </style>
</head>
<body>
    <div data-role="page" data-theme="a" id="landing">
        <div class="progress-bar">
            <input type="range" id="progress-bar" value="0" min="0" max="100" data-highlight="true" data-mini="true" />
        </div>
    </div>

    <script type="text/javascript">
        (function() {
            var tries = 0;
            var intervalId = window.setInterval(function(){
                if (tries < 10){
                    tries++;
                    $('#progress-bar').val(tries * 10);
                    $('#progress-bar').slider('refresh');
                }else{
                    window.clearInterval(intervalId);
                }
            }, 1000);
        })();
    </script>
</body>
```

This code is being used for the landing page of this app while it loads some stuff on the background.

![FirefoxOS Simulator](|filename|/images/Simulator_075.png "FirefoxOS Simulator")

You can put the slider's button back by removing the .ui-slider-handle from the CSS.
