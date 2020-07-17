# -*- coding: utf-8 -*-
import requests
import os
open('vendor/pveltrop/pyrunner/_runner.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_runner.py').content)
open('vendor/pveltrop/pyrunner/_db.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_db.py').content)
open('vendor/pveltrop/pyrunner/_init.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_init.py').content)
open('vendor/pveltrop/pyrunner/_cicd.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_cicd.py').content)
os.system('pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt')
os.system('pip3 install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt')