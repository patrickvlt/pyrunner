# -*- coding: utf-8 -*-
import os
os.system('pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt')
import sys
import requests
import subprocess
import re
import pathlib
from pushbullet import Pushbullet

customArgs = []
customArgs.append('--record')
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
record = None

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

for customArg in customArgs:
    for sysArg in sys.argv:
        if sysArg == '--record':
            record = True

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
os.system("sudo service redis-server start")
os.system("redis-cli --version")
os.system("cp .env.testing .env")
# Get from .env
f = open(('.env'), 'r')
env = f.read()
DB_ROW = FindENV("DB_DATABASE",env)
URL_ROW = FindENV("APP_URL",env)
DB_ENV = FindValue("DB_DATABASE",env)
# Get from .yml
f = open(('.gitlab-ci.yml'), 'r')
yml = f.read()
DB_YML = FindYML("MYSQL_DATABASE",yml)
DBPASS_YML = FindYML("MYSQL_ROOT_PASSWORD",yml)
DB_DATABASE = DB_ROW.replace(DB_ENV,DB_YML)
f = open(('.env'), 'r')
oldContent = f.read()
newContent = re.sub(DB_ROW, DB_DATABASE, oldContent)
newContent = re.sub('DB_PASSWORD=', 'DB_PASSWORD='+str(DBPASS_YML), newContent)
newContent = re.sub(URL_ROW, 'APP_URL=http://localhost', newContent)
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
if os.system('composer install') > 0:
    TestFailed()
if os.system('php artisan key:generate') > 0:
    TestFailed()
if os.system('php artisan config:clear') > 0:
    TestFailed()
if os.system('php artisan migrate') > 0:
    TestFailed()
if os.system('php artisan migrate:rollback') > 0:
    TestFailed()
if os.system('php artisan migrate:fresh --seed') > 0:
    TestFailed()
if os.system('npm install') > 0:
    TestFailed()

def FindString(key,content):
    regex = r""+key+"=.*"
    match = re.search(regex, content)
    match = match.group()
    match = match.replace(key+'=','')
    return match

# Up or downgrade chromedriver-py if necessary
versionStr = subprocess.check_output(['google-chrome','--version'])
chromeVer = re.search(r"\s[\.,\d]*\s", str(versionStr))
chromeVer = chromeVer.group(0).strip()
print("Chrome Version: "+str(chromeVer))
os.system("pip install 'chromedriver-py<="+chromeVer+"' --force-reinstall")

# Get from .env
f = open(('.env'), 'r')
env = f.read()
WEB_URL = FindString("APP_URL",env)
SERVE_URL = FindString("APP_URL",env).split('//')[-1]

# Serve project
os.system("php artisan serve --port=80 --host=localhost &")

# Recording and running
if record is not None:
    print("Launching PyRunner with recording")
    os.system("sleep 1; ffmpeg -r 30 -f x11grab -draw_mouse 0 -s 1920x1080 -i :99 -c:v libvpx -quality realtime -cpu-used 0 -b:v 384k -qmin 42 -qmax 42 -maxrate 200k -bufsize 1000k -an record.mkv -nostdin &")
    exit_code = os.system("xvfb-run --server-num 99 --auth-file /tmp/xvfb.auth -s '-ac -screen 0 1920x1080x24' python vendor/pveltrop/pyrunner/test_app.py --debug --cicd")
    os.system("killall -r xvfb")
    os.system("killall -r ffmpeg")
    os.system('sudo find . -name "*record.mkv*"')
else:
    exit_code = os.system("python vendor/pveltrop/pyrunner/test_app.py --debug --shell --cicd --screenshots")

if exit_code > 0:
    TestFailed()
else:
    TestSucceeded()

exit()
