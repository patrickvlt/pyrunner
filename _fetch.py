# -*- coding: utf-8 -*-
import requests
import os

print("foo")

runnerContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_runner.py').content
if '404' not in runnerContent:
    open('vendor/pveltrop/pyrunner/_runner.py', 'wb').write(runnerContent)
    
dbContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_db.py').content
if '404' not in dbContent:
    open('vendor/pveltrop/pyrunner/_db.py', 'wb').write(dbContent)
    
initContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_init.py').content
if '404' not in initContent:
    open('vendor/pveltrop/pyrunner/_init.py', 'wb').write(initContent)
    
cicdContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_cicd.py').content
if '404' not in cicdContent:
    open('vendor/pveltrop/pyrunner/_cicd.py', 'wb').write(cicdContent)
    
updateContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_update.py').content
if '404' not in updateContent:
    open('vendor/pveltrop/pyrunner/_update.py', 'wb').write(updateContent)
    
# Service Provider

providerContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/PyRunnerProvider.php').content
if '404' not in providerContent:
    open('vendor/pveltrop/pyrunner/src/PyRunnerProvider.php', 'wb').write(providerContent)
    
# Commands
    
installCmdContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Install.php').content
if '404' not in installCmdContent:
    open('vendor/pveltrop/pyrunner/src/app/Commands/Install.php', 'wb').write(installCmdContent)
    
startCmdContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Start.php').content
if '404' not in startCmdContent:
    open('vendor/pveltrop/pyrunner/src/app/Commands/Start.php', 'wb').write(startCmdContent)
    
updateCmdContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Update.php').content
if '404' not in updateCmdContent:
    open('vendor/pveltrop/pyrunner/src/app/Commands/Update.php', 'wb').write(updateCmdContent)
