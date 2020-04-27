# -*- coding: utf-8 -*-
# Python 3.8.1

import os
import sys
import requests
from pushbullet import Pushbullet

customArgs = []
customArgs.append('--project=')
customArgs.append('--url=')
customArgs.append('--branch=')
customArgs.append('--author=')
customArgs.append('--pushbullet=')
customArgs.append('--slack=')

thisProject = None
thisUrl = None
thisBranch = None
thisAuthor = None
thisPushbullet = None
thisSlack = None
thisPbchannel = None

for customArg in customArgs:
    for sysArg in sys.argv:
        sysArg = sysArg.split('=')
        cmd = sysArg[0]
        try:
            val = sysArg[1]
        except:
            continue
        if cmd in customArg:
            if cmd == '--project':
                thisProject = val
            if cmd == '--url':
                thisUrl = val
            if cmd == '--branch':
                thisBranch = val
            if cmd == '--author':
                thisAuthor = val
            if cmd == '--pushbullet':
                thisPushbullet = val
            if cmd == '--pbchannel':
                thisPbchannel = val
            if cmd == '--slack':
                thisSlack = val

setup = 1

# Sets up the Jottenheijm channel for Pushbullet and Slack
headers = {'Content-type': 'application/json', }
fail_msg = thisProject+": Testing branch failed: "+thisBranch+" by "+thisAuthor+" --> "+thisUrl+""
succeed_msg = thisProject+": Testing branch succeeded: "+thisBranch+" by "+thisAuthor+" --> "+thisUrl+""
if thisPushbullet is not None and thisPbchannel is not None:
    pb = Pushbullet(thisPushbullet)
    for channel in pb.channels:
        if str(thisPbchannel) in str(channel):
            pushbullet = channel

# Run python file which runs defined test functions
exit_code = os.system("python vendor/pveltrop/pyrunner/test_app.py debug shell")

# Returns exit code for GitLab and sends message to Slack or Pushbullet
if exit_code > 0:
    print("Test Failed")
    if thisPushbullet is not None and thisPbchannel is not None:
        pushbullet = pushbullet.push_link(thisProject+": Testing Failed", thisUrl, "Author: " + thisAuthor + " (" + thisBranch + ")")
    if thisSlack is not None:
        slack = requests.post(thisSlack, headers=headers, data='{"text":"'+fail_msg+'"}')
    sys.exit(1)
    exit()
else:
    if thisPushbullet is not None and thisPbchannel is not None:
        pushbullet = pushbullet.push_link(thisProject+": Testing Succeeded", thisUrl, "Author: " + thisAuthor + " (" + thisBranch + ")")
    if thisSlack is not None:
        slack = requests.post(thisSlack, headers=headers, data='{"text":"'+succeed_msg+'"}')
    sys.exit(0)
    exit()

exit()
