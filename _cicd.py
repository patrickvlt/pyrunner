# -*- coding: utf-8 -*-
import os
os.system('pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt')
import sys
import requests
import subprocess
import re
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

def FindYML(key,content):
    regex = r""+key+": .*"
    match = re.search(regex, content)
    match = match.group()
    match = match.replace(key+': ','')
    return match

def FindValue(key,content):
    regex = r""+key+"=.*"
    match = re.search(regex, content)
    match = match.group()
    match = match.replace(key+'=','')
    return match

def FindENV(key,content):
    regex = r""+key+"=.*"
    match = re.search(regex, content)
    match = match.group()
    return match

# Overwrite DB_DATABASE in the .env with the one from the .yml
os.system("sudo systemctl restart redis-server.service")
os.system("cp .env.testing .env")
# Get from .env
f = open(('.env'), 'r')
env = f.read()
DB_ROW = FindENV("DB_DATABASE",env)
DBPASS_ROW = FindENV("DB_PASSWORD",env)
DB_ENV = FindValue("DB_DATABASE",env)
DBPASS_ENV = FindValue("DB_PASSWORD",env)
# Get from .yml
f = open(('.gitlab-ci.yml'), 'r')
yml = f.read()
DB_YML = FindYML("MYSQL_DATABASE",yml)
DBPASS_YML = FindYML("MYSQL_ROOT_PASSWORD",yml)
DB_DATABASE = DB_ROW.replace(DB_ENV,DB_YML)
DB_PASSWORD = DBPASS_ROW.replace(DBPASS_ENV,DBPASS_YML)
f = open(('.env'), 'r')
oldContent = f.read()
newContent = re.sub(DB_ROW, DB_DATABASE, oldContent)
newContent = re.sub(DBPASS_ROW, DB_PASSWORD, newContent)
open_file = open('.env', "wt")
open_file.write(newContent)
open_file.close()

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
    ComposerMigrate = 'composer install; php artisan key:generate; php artisan config:clear; php artisan migrate; php artisan migrate:rollback; php artisan migrate:fresh --seed'
    NPM = 'npm install'
    ChromeDriver = 'wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; sudo dpkg -i google-chrome-stable_current_amd64.deb; google-chrome --version'

    jobs = [ComposerMigrate, NPM, ChromeDriver]

    ps = []

    for job in jobs:
        p = subprocess.Popen([job],shell=True)
        ps.append(p)

    for p in ps:
        p.wait()
    
except Exception as e:
    print(e)
    TestFailed()
    
def FindString(key,content):
    regex = r""+key+"=.*"
    match = re.search(regex, content)
    match = match.group()
    match = match.replace(key+'=','')
    return match

# Get from .env
f = open(('.env'), 'r')
env = f.read()
SERVE_URL = FindString("APP_URL",env).split('//')[-1]

# Run python file which runs defined test functions
exit_code = os.system("php artisan serve --port=80 --host="+str(SERVE_URL)+" & python vendor/pveltrop/pyrunner/test_app.py --debug --shell")
    
if exit_code > 0:
    TestFailed()
else:
    TestSucceeded()

exit()
