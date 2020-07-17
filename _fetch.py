# -*- coding: utf-8 -*-
import requests
import os

print("foo")
    
runnerContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_runner.py').content
runnerStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_runner.py').status_code
if runnerStatus != 404:
    open('vendor/pveltrop/pyrunner/_runner.py', 'wb').write(runnerContent)
    
dbContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_db.py').content
dbStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_db.py').status_code
if dbStatus != 404:
    open('vendor/pveltrop/pyrunner/_db.py', 'wb').write(dbContent)
    
initContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_init.py').content
initStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_init.py').status_code
if initStatus != 404:
    open('vendor/pveltrop/pyrunner/_init.py', 'wb').write(initContent)
    
cicdContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_cicd.py').content
cicdStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_cicd.py').status_code
if cicdStatus != 404:
    open('vendor/pveltrop/pyrunner/_cicd.py', 'wb').write(cicdContent)
    
updateContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_update.py').content
updateStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_update.py').status_code
if updateStatus != 404:
    open('vendor/pveltrop/pyrunner/_update.py', 'wb').write(updateContent)
    
# Service Provider

providerContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_provider.py').content
providerStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_provider.py').status_code
if providerStatus != 404:
    open('vendor/pveltrop/pyrunner/_provider.py', 'wb').write(providerContent)
    
# Commands
    
InstallContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Install.php').content
InstallStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Install.php').status_code
if InstallStatus != 404:
    open('vendor/pveltrop/pyrunner/src/app/Commands/Install.php', 'wb').write(InstallContent)
    
StartContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Start.php').content
StartStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Start.php').status_code
if StartStatus != 404:
    open('vendor/pveltrop/pyrunner/src/app/Commands/Start.php', 'wb').write(StartContent)
    
UpdateContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Update.php').content
UpdateStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/src/app/Commands/Update.php').status_code
if UpdateStatus != 404:
    open('vendor/pveltrop/pyrunner/src/app/Commands/Update.php', 'wb').write(UpdateContent)
