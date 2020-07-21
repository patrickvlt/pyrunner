# -*- coding: utf-8 -*-
import requests

fetchContent = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_fetch.py').content
fetchStatus = requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_fetch.py').status_code
if fetchStatus != 404:
    open('vendor/pveltrop/pyrunner/_fetch.py', 'wb').write(fetchContent)
    import _fetch
