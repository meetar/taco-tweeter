#!/usr/bin/python

import cgi, twython, json
from twython import Twython, TwythonError

form = cgi.FieldStorage()
payload = form["payload"].value
myjson = json.loads(payload)

# check to make sure this is being called by tacofancy
# (primitive and easily-spoofed security measure)
repo = myjson["repository"]["url"]
if repo != "https://github.com/sinker/tacofancy":
  sys.exit()

commits = myjson["commits"]

addeds = []

# make a list of commits with added files
for item in commits:
  if item["added"] != []:
    addeds.append(item)

# find the second-to-last commit; the last commit will be the merge,
# which will have extra "merging" messages. We just want the message
# of the source commit.
last = len(addeds) - 2

lastcommit = addeds[last]

# assemble the tweet
message = lastcommit["message"]
url = lastcommit["url"]

newstatus = lastcommit["message"] + " " + lastcommit["url"]



# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
APP_KEY="XXXXXXXXXXXXXXXXXXXXXX"
APP_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
OAUTH_TOKEN="9999999999-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
OAUTH_TOKEN_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# tweet it
try:
  twitter.update_status(status=newstatus)
except Exception, exception:
  print "Error:"
  print exception
