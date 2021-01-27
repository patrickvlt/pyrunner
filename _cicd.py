# -*- coding: utf-8 -*-
import os
os.system('pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt')
import sys
import requests
import subprocess
import re
import pathlib

customArgs = []
customArgs.append('--record')
customArgs.append('--pyrunner')
customArgs.append('--phpunit')

Pyrunner = None
PHPunit = None
record = None

for customArg in customArgs:
    for sysArg in sys.argv:
        if sysArg == '--record':
            record = True
        if sysArg == '--pyrunner':
            Pyrunner = True
        if sysArg == '--phpunit':
            PHPunit = True
        if sysArg == '--install':
            installProject = True

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

# Returns exit code for GitLab
def TestFailed():
    sys.exit(1)
    exit()

def TestSucceeded():
    sys.exit(0)
    exit()

# Prepare Laravel
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
    

# This will change if tests fail
exit_code = 1

def LaunchPyrunner():
    # Up or downgrade chromedriver-py if necessary
    versionStr = subprocess.check_output(['google-chrome','--version'])
    chromeVer = re.search(r"\s[\.,\d]*\s", str(versionStr))
    chromeVer = chromeVer.group(0).strip()
    print("Chrome Version: "+str(chromeVer))
    os.system("pip install 'chromedriver-py<="+chromeVer+"' --force-reinstall")

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
        return os.system("python vendor/pveltrop/pyrunner/test_app.py --debug --shell --cicd --screenshots")
        
def LaunchPHPUnit():
    return os.system("XDEBUG_MODE=coverage vendor/bin/phpunit --colors --debug --coverage-html reports/")

if Pyrunner is not None:
    exit_code = LaunchPyrunner()
    
if PHPunit is not None:
    exit_code = LaunchPHPUnit()
    
if exit_code > 0:
    sys.exit(1)
else:
    sys.exit(0)
