taco-tweeter
============

A WebHook for [Tacofancy](http://github.com/sinker/tacofancy/) – this tweets to [@TacoBot](http://twitter.com/TacoBot) when a new file is added to the repo.

To use this repo
----------------

1. Host one of the included .cgi files on a public server. Make sure it has the executable flags set: (chmod filename 755)
2. Set up a Twitter app at https://dev.twitter.com/apps and link it to the twitter account of your choice. Make sure the application type is "Read and write", then update the settings and make a note of the OAuth credentials under the "OAuth tool" tab.
3. Add the OAuth credentials to the .cgi.
3. Add the URL of the .cgi file as a WebHook URL in your github repo's settings: https://github.com/[username]/[reponame]/settings/hooks

When you merge a pull request or otherwise push to your repo, GitHub will use the WebHook to send a POST request to your .cgi file, with a json-formatted collection of information about the push, including commits, commit messages, user information, and whether files were added or removed.

As it's written, this particular .cgi is set to only accept data about the tacofancy repo, and expects that pushes will mostly be the result of pull requests. YMMV.
