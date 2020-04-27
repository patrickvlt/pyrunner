# -----------------------------------------------------------
# Request Examples To Laravel Routes
# -----------------------------------------------------------

import requests
import json

#PHP string
r = requests.get('http://localhost/_testing/pystring').text
print(r)

#PHP array
r = requests.get('http://localhost/_testing/pyphparray').text
r = json.loads(r)
print(r)

for x in r:
    print(x)

#JSON string
r = requests.get('http://localhost/_testing/pyjsonstring').text
print(r)

#JSON array
r = requests.get('http://localhost/_testing/pyjsonarray').text
r = json.loads(r)
for x in r:
    print(x)