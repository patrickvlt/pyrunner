# -*- coding: utf-8 -*-
import _init as pr
import _tests as tests

# -----------------------------------------------------------
# Define which tests you want to run
# -----------------------------------------------------------

if pr.dev is None:
    tests.RunTests()
    pr.finished()

else:
    print(' ')
    print(pr.Fore.CYAN+'Developing mode initialised')
    print('You can run tests individually, or run commands in _tests.py to make a new test, step by step')
    print('For example, try to run a test from the list in test_app.py, just type the following: tests.(name_of_your_test)()')
    print('Or try to run a single command (located in _tests.py), for example: pr.click(element_to_click)'+pr.Style.RESET_ALL)
    print(' ')
    pr.ipdb.set_trace(context=1)

