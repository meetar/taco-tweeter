taco-tweeter
============

A WebHook for [Tacofancy](http://github.com/sinker/tacofancy/) – this tweets to [@taco_fancy](http://twitter.com/taco_fancy) when a new file is added to the repo.

To use this repo
----------------

1. Host one of the included .cgi files on a public server. Make sure it has the executable flags set: (chmod filename 755)
2. Set up a Twitter app at https://dev.twitter.com/apps and link it to the twitter account of your choice. Make sure the application type is "Read and write", then update the settings and make a note of the OAuth credentials under the "OAuth tool" tab.
3. Add the OAuth credentials to the .cgi.
3. Add the URL of the .cgi file as a WebHook URL in your github repo's settings: https://github.com/[username]/[reponame]/settings/hooks

When you merge a pull request or otherwise push to your repo, GitHub will use the WebHook to send a POST request to your .cgi file, with a json-formatted collection of information about the push, including commits, commit messages, user information, and whether files were added or removed.

As it's written, this particular .cgi is set to only accept data about the tacofancy repo, and expects that pushes will mostly be the result of pull requests. YMMV.

## Setting up and deploying as a Flask app

Clone this repo and setup a python virtualenv (entirely optional but makes things saner):

``` bash
$ git clone https://github.com/meetar/taco-tweeter.git
$ virtualenv venv .
$ source venv/bin/activate
```

``pip install`` the requirements:

``` bash
$ pip install -r requirements.txt
```

Before actually running the application, you’ll need to setup the Twitter
API credentials and OAuth credentials as environmental variables. A simple
way to do this is to place them into the ``.bashrc`` of the user that will
be running the application. If you’re deploying this app onto Heroku, you
can set these by running:

``` bash
$ heroku config:set TWITTER_API_KEY='your API key here'
$ heroku config:set TWITTER_API_SECRET='your API secret here'
$ heroku config:set TWITTER_OAUTH_TOKEN='your OAuth token here'
$ heroku config:set TWITTER_OAUTH_TOKEN_SECRET='you OAuth secret here'
```

Locally you can run the app by running ``python app.py`` or by using gunicorn:

``` bash
$ gunicorn app:app
```

There is also a ``Procfile`` included so that deploying it to Heroku should be
pretty simple.


