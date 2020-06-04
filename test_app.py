# -*- coding: utf-8 -*-
import requests
open('_init.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_init.py').content)

import _init as pr
import _tests as tests

tests.RunTests()
