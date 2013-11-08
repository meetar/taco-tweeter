#!/usr/bin/python

import cgi, twython, json
from twython import Twython, TwythonError

open('err', 'w').close()

f = open('err', 'rw+')

form = cgi.FieldStorage()
payload = form["payload"].value
myjson = json.loads(payload)

repo = myjson["repository"]["url"]
f.write("repo:\n")
f.write(str(repo))
f.write("\n\n")

# check to make sure this is being called by tacofancy
# (primitive and easily-spoofed security measure)
if repo != "https://github.com/sinker/tacofancy":
  f.write("wrong repo, exiting")
  f.close()
  sys.exit()
else:
  f.write("carry on\n")


commits = myjson["commits"]

f.write("payload:\n")
f.write(str(payload))
f.write("\n\n")

f.write("commits?\n")
f.write(str(commits))
f.write("\n\n")

f.write("len(commits)?\n")
f.write(str(len(commits)))
f.write("\n")

addeds = []

# make a list of commits with added files
for item in commits:
  f.write(str(i)+"\n")
  f.write(str(item["added"]))
  f.write("\n")
  if item["added"] != []:
    f.write("-- ADDED --\n")
    f.write(str(item["added"])+"\n")
    addeds.append(item)
    f.write("\n")


f.write("\n\n")
f.write("addeds:\n")

f.write(str(addeds))

# find the second-to-last commit; the last commit will be the merge,
# which will have extra "merging" messages. We just want the message
# of the source commit.
last = len(addeds) - 2

f.write("addeds[length]?\n")
f.write(str(addeds[last]))
f.write("\n\n")

lastcommit = addeds[last]

f.write("last commit\n")
f.write(str(lastcommit))
f.write("\n\n")

# assemble the tweet
message = lastcommit["message"]
url = lastcommit["url"]

f.write(str(message))
f.write("\n")
f.write(str(url))
f.write("\n\n")

newstatus = lastcommit["message"] + " " + lastcommit["url"]

f.write("newstatus:\n")
f.write(str(newstatus))
f.write("\n\n")

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
  f.write(str(exception))
  print exception
  
f.close()
