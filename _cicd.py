# -*- coding: utf-8 -*-

import os
os.system('pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt')
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
customArgs.append('--pbchannel=')

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
            
# Returns exit code for GitLab and sends message to Slack or Pushbullet
def TestFailed():
    print("Test Failed")
    if thisPushbullet is not None and thisPbchannel is not None:
        pushbullet.push_link(thisProject+": Testing Failed", thisUrl, "Author: " + thisAuthor + " (" + thisBranch + ")")
    if thisSlack is not None:
        slack = requests.post(thisSlack, headers=headers, data='{"text":"'+fail_msg+'"}')
    sys.exit(1)
    exit()
    
def TestSucceeded():
    if thisPushbullet is not None and thisPbchannel is not None:
        pushbullet.push_link(thisProject+": Testing Succeeded", thisUrl, "Author: " + thisAuthor + " (" + thisBranch + ")")
    if thisSlack is not None:
        slack = requests.post(thisSlack, headers=headers, data='{"text":"'+succeed_msg+'"}')
    sys.exit(0)
    exit()
            
# Prepare Laravel
try:
    os.system('cp .env.testing .env')
    os.system('php artisan key:generate')
    os.system('php artisan config:clear')
    os.system('php artisan migrate:fresh --seed')
    os.system('php artisan migrate:rollback')
    os.system('php artisan migrate:fresh --seed')
    os.system('npm install')
    os.system('sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
    os.system('sudo apt install -y ./google-chrome-stable_current_amd64.deb')
except Exception as e:
    print(e)
    TestFailed()

# Run python file which runs defined test functions
exit_code = os.system("php artisan serve --port=80 --env=testing --host=localhost & python vendor/pveltrop/pyrunner/test_app.py debug shell")
    
if exit_code > 0:
    TestFailed()
else:
    TestSucceeded()

exit()
