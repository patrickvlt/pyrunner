# -*- coding: utf-8 -*-

# load tests and chromedriver
try:
    from importlib import reload
except:
    print('Reloading module couldn\'t be loaded. Dev mode won\'t see file changes.')

import _init as pr
import _tests as tests
import sys, inspect, re

customArgs = []
customArgs.append('--group=')

thisGroup = None
testList = []
failedTests = []

for customArg in customArgs:
    for sysArg in sys.argv:
        sysArg = sysArg.split('=')
        cmd = sysArg[0]
        try:
            val = sysArg[1]
        except:
            continue
        if cmd in customArg:
            if cmd == '--group':
                thisGroup = val
                
sourceTests = inspect.getsource(tests.RunTests)
definedTests = re.finditer(r".*_\S*\(.*\)", sourceTests, re.MULTILINE)
for definedTest in definedTests:
    if "#" not in definedTest.group():
        testList.append(definedTest.group())

# dev mode
def DevMode():
    print(pr.Fore.CYAN+'Developing mode initialised')
    print(' ')
    print(' ')
    print('To run a single PyRunner cmd: pr.click(element_to_click)'+pr.Style.RESET_ALL)
    print(' ')
    print('To run a single test, reload your defined tests: ')
    print('reload(tests)')
    print('Then run your test:')
    print('tests.yourTestName(parameters)')
    print(' ')
    print('To run all your tests:')
    print('RunTests()')
    print(' ')
    pr.ipdb.set_trace(context=1)
    
def RunTests():
    try:
        reload(tests)
    except:
        print('')
    for definedTest in testList:
        if "#" not in definedTest:
            try:
                cmd = 'tests.'+definedTest
                exec(cmd)
            except Exception as e:
                if pr.screenshots is not None:
                    pr.browser.save_screenshot('pyrunner/failed_step_'+str(pr.current_step)+'.png')
                print(' ')
                print(pr.Style.RESET_ALL+'Failed at step '+str(pr.current_step)+': '+pr.Fore.RED+str(pr.current_test)+pr.Style.RESET_ALL)
                print(pr.Style.RESET_ALL+'Error: '+pr.Fore.RED+str(e)+pr.Style.RESET_ALL)
                print(' ')
                print(' ')
                failedTests.append({
                    'test': definedTest,
                    'name': pr.current_test,
                    'error': e,
                    'step': pr.current_step,
                })
                pass
        exit
    if not failedTests:
        pr.finished()
    else:
        if pr.dev is not None:
            for failed in failedTests:
                print(' ')
                print(pr.Style.RESET_ALL+'Failed test at step '+str(failed['step'])+': '+pr.Fore.RED+str(failed['name'])+pr.Style.RESET_ALL)
                print(pr.Style.RESET_ALL+'Error: '+pr.Fore.RED+str(failed['error'])+pr.Style.RESET_ALL)
                print(' ')
                print(' ')
            DevMode()
        else:
            pr.failed(failedTests)
            
def RunSingleTest(thisGroup):
    try:
        reload(tests)
    except:
        print('')
    try:
        exec('test.Group'+str(thisGroup)+'()')
        pr.finished(str(thisGroup))
    except Exception as e:
        pr.failed(e)


if pr.dev is not None:
    if thisGroup is not None:
        RunSingleTest(thisGroup)
    else:
        DevMode()
else:
    if thisGroup is not None:
        RunSingleTest(thisGroup)
    else:
        RunTests()
