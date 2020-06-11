# -*- coding: utf-8 -*-

# update core from github

import requests
import requests
open('vendor/pveltrop/pyrunner/_dbexport.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_dbexport.py').content)
open('vendor/pveltrop/pyrunner/_init.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_init.py').content)
open('vendor/pveltrop/pyrunner/_cicd.py', 'wb').write(requests.get('https://raw.githubusercontent.com/43874/pyrunner/master/_cicd.py').content)

# load tests and chromedriver
try:
    from importlib import reload
except:
    print('Reloading module couldn\'t be loaded. Dev mode won\'t see file changes.')

import _init as pr
import _tests as test


# dev mode
def DevMode():
    print(' ')
    print(pr.Fore.CYAN+'Developing mode initialised')
    print('You can run tests individually, or run commands in _tests.py to make a new test, step by step')
    print(' ')
    print('For example, try to run a test from the list in test_app.py, enter: ')
    print('test.(name_of_your_test)()')
    print(' ')
    print('To run all your tests, enter:')
    print('RunTests()')
    print(' ')
    print('Or try to run a single command (located in _tests.py), for example: pr.click(element_to_click)'+pr.Style.RESET_ALL)
    print(' ')
    pr.ipdb.set_trace(context=1)
    
def RunTests():
    try:
        reload(test)
    except:
        print('')
    try:
        test.RunTests()
        pr.finished()
    except Exception as e:
        if pr.dev is not None:
            print(' ')
            print(' ')
            print(pr.Fore.RED+str(e)+pr.Style.RESET_ALL)
            DevMode()
        else:
            pr.failed(e)

if pr.dev is not None:
    DevMode()
else:
    RunTests()
