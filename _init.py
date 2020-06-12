# -*- coding: utf-8 -*-
# coding=utf8

# -----------------------------------------------------------
# Requirements & Init
# -----------------------------------------------------------

import time
import json
import sys
import os
import re
import glob
import xlwt
import ipdb 
import shutil

from os.path import basename
from zipfile import ZipFile
from datetime import datetime
from datetime import date
from selenium import webdriver
from colorama import init, Fore, Back, Style
from retrying import retry
from chromedriver_py import binary_path
from selenium.webdriver.support.ui import WebDriverWait
from xlwt import Workbook

init()

shutil.rmtree('pyrunner', ignore_errors=True)
os.system('mkdir pyrunner')

# -----------------------------------------------------------
# Set Up Browser
# -----------------------------------------------------------

customArgs = []
customArgs.append('dev')

dev = None
shell = None
debug = None

for customArg in customArgs:
    for sysArg in sys.argv: 
        if sysArg == 'dev':
            dev = True
        if sysArg == 'shell':
            shell = True
        if sysArg == 'debug':
            debug = True

if shell is not None:
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('window-size=1920x1080')
    if dev is not None:
        max_retries = 0
    else:
        max_retries = 3
else:
    options = None
    max_retries = 0
    
browser = webdriver.Chrome(executable_path=binary_path,options=options)
browser.implicitly_wait(10)
browser.get('http://localhost/')
browser.maximize_window()

# -----------------------------------------------------------
# Functions which execute browser commands
# -----------------------------------------------------------
    
current_step = 0
current_cmd = 0
test_time=datetime.now()
failProject = None
step_desc = None
current_test = None

def wait_ajax(timeout=15):
    wait = WebDriverWait(browser, timeout)
    try:
        wait.until(lambda browser: browser.execute_script('return jQuery.active') == 0)
        wait.until(lambda browser: browser.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass
    
def get(url=''):
    wait_ajax(20)
    browser.get(url)
    
@retry(stop_max_attempt_number=max_retries)
def click(xpath=None, css=None, id=None):
    wait_ajax()
    time.sleep(0.5)
    def Click(css, xpath, id):
        try:
            if debug is not None:
                print('Trying to click by CSS with Selenium on: '+str(css))
            browser.find_element_by_css_selector(css).click()
            if debug is not None:
                print(Fore.GREEN+'Clicked with css, returning'+Style.RESET_ALL)
            return
        except:
            if debug is not None:
                print('CSS click failed with: ' + str(css))
        try:
            if debug is not None:
                print('Trying to click by CSS with JS on: '+str(css))
            browser.execute_script('document.querySelectorAll("'+css+'").click()')
            if debug is not None:
                print(Fore.GREEN+'Clicked with css, returning'+Style.RESET_ALL)
            return
        except:
            if debug is not None:
                print('CSS click failed with: ' + str(css))
        if xpath is not None:
            try:
                if debug is not None:
                    print('Trying to click by Xpath on: '+str(xpath))
                browser.find_element_by_xpath(xpath).click()
                if debug is not None:
                    print(Fore.GREEN+'Clicked with Xpath, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print('Xpath click failed with: ' + str(xpath))
        if id is not None:
            try:
                if debug is not None:
                    print('Trying to click with ID on: '+'//*[@id="'+id+'"]')
                browser.find_element_by_xpath('//*[@id="'+id+'"]').click()
                if debug is not None:
                    print(Fore.GREEN+'Clicked with ID, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print('ID click failed with: ' + str(id))
            try:
                if debug is not None:
                    print('Trying to click by ID on: '+str(id))
                browser.find_element_by_id(id).click()
                if debug is not None:
                    print(Fore.GREEN+'Clicked with ID, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print('ID click failed with: ' + str(id))
            try:
                if debug is not None:
                    print('Trying to click by ID by executing script: '+"document.getElementById('"+id+"').click()")
                browser.execute_script("document.getElementById('"+id+"').click()")
                if debug is not None:
                    print(Fore.GREEN+'Clicked with browser script, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print('ID click failed with: ' + str(id))
                raise TypeError("Can't click this element: "+str(id)+".")
    Click(css, xpath, id)

@retry(stop_max_attempt_number=max_retries)
def switch_tab(index):
    wait_ajax()
    browser.switch_to.window(browser.window_handles[index])

# Selecting

@retry(stop_max_attempt_number=max_retries)
def select_value_name(name, value):
    wait_ajax()
    if debug is not None:
        print('Selecting '+str(value)+' in '+str(name))
    browser.find_element_by_xpath(
        "//select[@name='"+name+"']/option[@value='"+value+"']").click()

@retry(stop_max_attempt_number=max_retries)
def select_index_name(name, index):
    wait_ajax()
    if debug is not None:
        print('Selecting '+str(index)+' in '+str(name))
    browser.find_element_by_xpath(
        "//select[@name='"+name+"']/option["+index+"]").click()
    
@retry(stop_max_attempt_number=max_retries)
def select_value_id(id, value):
    wait_ajax()
    if debug is not None:
        print('Selecting '+str(value)+' in '+str(id))
    browser.find_element_by_xpath(
        "//select[@id='"+id+"']/option[@value='"+value+"']").click()

@retry(stop_max_attempt_number=max_retries)
def select_index_id(id, index):
    wait_ajax()
    if debug is not None:
        print('Selecting '+str(index)+' in '+str(id))
    browser.find_element_by_xpath(
        "//select[@id='"+id+"']/option["+index+"]").click()
    
# Finding elements, these functions will retry based on the timeout variable you send along
def find_text(text, timeout = 2):
    wait_ajax()
    @retry(stop_max_attempt_number=timeout)
    def wait(text):
        if debug is not None:
            print('Trying to find text: '+str(text))
        element = browser.find_element_by_xpath(
            "//*[contains(text(), '"+text+"')]")
        if element.is_displayed() is False:
            return False
        wait(text)


def find_id(id, timeout = 2):
    wait_ajax()
    @retry(stop_max_attempt_number=timeout)
    def wait(id):
        if debug is not None:
            print('Trying to find ID: '+str(id))
        element = browser.find_element_by_id(id)
        if element.is_displayed() is True:
            print('Found ID: '+id)
        else:
            return False
    wait(id)


def find_class(el_class, timeout = 2):
    wait_ajax()
    @retry(stop_max_attempt_number=timeout)
    def wait(el_class):
        if debug is not None:
            print('Trying to find class: '+str(el_class))
        element = browser.find_element_by_class_name(el_class)
        if element.is_displayed() is True:
            print('Found class: '+el_class)
        else:
            return False
    wait(el_class)


def find_css(css, timeout = 2):
    wait_ajax()
    @retry(stop_max_attempt_number=timeout)
    def wait(css):
        if debug is not None:
            print('Trying to find css: '+str(css))
        element = browser.find_element_by_css_selector(css)
        if element.is_displayed() is True:
            print('Found CSS: '+css)
        else:
            return False
    wait(css)


def find_name(name, timeout = 2):
    wait_ajax()
    @retry(stop_max_attempt_number=timeout)
    def wait(name):
        if debug is not None:
            print('Trying to find name: '+str(name))
        element = browser.find_element_by_name(name)
        if element.is_displayed() is True:
            print('Found name: '+name)
        else:
            return False
    wait(name)
    
def find_xpath(xpath, timeout = 2):
    wait_ajax()
    @retry(stop_max_attempt_number=timeout)
    def wait(xpath):
        if debug is not None:
            print('Trying to find Xpath: '+str(xpath))
        element = browser.find_element_by_xpath(xpath)
        if element.is_displayed() is True:
            print('Found XPath: '+xpath)
        else:
            return False
    wait(xpath)

# Typing

@retry(stop_max_attempt_number=max_retries)
def type_xpath(xpath, value):
    wait_ajax()
    if debug is not None:
            print('Trying to type: '+str(value)+' in '+str(xpath))
    browser.find_element_by_xpath(xpath).send_keys(value)


@retry(stop_max_attempt_number=max_retries)
def type_name(name, value):
    wait_ajax()
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(name))
    browser.find_element_by_name(name).send_keys(value)


@retry(stop_max_attempt_number=max_retries)
def type_id(id, value):
    wait_ajax()
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(id))
    browser.find_element_by_id(id).send_keys(value)


@retry(stop_max_attempt_number=max_retries)
def type_css(css, value):
    wait_ajax()
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(css))
    browser.find_element_by_css_selector(css).send_keys(value)
    
# Clearing and Typing
@retry(stop_max_attempt_number=max_retries)
def change_text_xpath(xpath, value):
    wait_ajax()
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(xpath))
    browser.find_element_by_xpath(xpath).clear()
    browser.find_element_by_xpath(xpath).send_keys(value)
    
@retry(stop_max_attempt_number=max_retries)
def change_text_name(name, value):
    wait_ajax()
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(name))
    browser.find_element_by_name(name).clear()
    browser.find_element_by_name(name).send_keys(value)
    
@retry(stop_max_attempt_number=max_retries)
def change_text_id(id, value):
    wait_ajax()
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(id))
    browser.find_element_by_id(id).clear()
    browser.find_element_by_id(id).send_keys(value)
    
@retry(stop_max_attempt_number=max_retries)
def change_text_css(css, value):
    wait_ajax()
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(css))
    browser.find_element_by_css_selector(css).clear()
    browser.find_element_by_css_selector(css).send_keys(value)

# -----------------------------------------------------------
# Code refactoring
# -----------------------------------------------------------

def scan_regex(regex):
    # Laravel variables
    laravelFolders = [
        'app', 'bootstrap', 'config', 'database', 'public', 'resources', 'routes'
    ]
    laravelFiles = []
    failProject = 0

    def LoopFolders(laravelFolders):
        for folder in laravelFolders:
            for currentpath, folders, files in os.walk(folder):
                for file in files:
                    if '.php' in str(file):
                        laravelFiles.append(os.path.join(currentpath, file))
    LoopFolders(laravelFolders)
    # Loop through Laravel Folders and fetch php files if one of the above folders is used
    if len(laravelFiles) == 0:
        newFolders = []
        for folder in laravelFolders:
            newFolders.append("../"+str(folder))
        LoopFolders(newFolders)

    # Scan for provided RegEx in all files
    for file in laravelFiles:
        f = open((file), 'r')
        x = 0
        for line in f:
            x = x + 1
            match = re.search(regex, line)
            if match is not None:
                if '//' not in str(line):
                    print(Fore.RED+str(file)+":"+str(x)+Style.RESET_ALL +
                        " has invalid code: " + Fore.RED + match.group())
                    failProject = 1
        f.close()

    if failProject >= 1:
        raise TypeError(Style.RESET_ALL+'This project contains code which should be ' +
                        Fore.RED+'removed'+Style.RESET_ALL)

# Replacing code
def replace_regex(find_regex, replace_regex, regex_file=None):
    # Laravel variables
    laravelFolders = [
        'app', 'bootstrap', 'config', 'database', 'public', 'resources', 'routes'
    ]
    laravelFiles = []
    failProject = 0

    # Loop through provided folders
    def LoopFolders(laravelFolders):
        for folder in laravelFolders:
            for currentpath, folders, files in os.walk(folder):
                for file in files:
                    if '.php' in str(file):
                        laravelFiles.append(os.path.join(currentpath, file))
    LoopFolders(laravelFolders)

    # If no folders are found, move up one parent
    if len(laravelFiles) == 0:
        newFolders = []
        for folder in laravelFolders:
            newFolders.append("../"+str(folder))
        LoopFolders(newFolders)

    # Replace content
    def ChangeFile(file):
        try:
            # Open and read content in file
            open_file = open(file, "rt")
            file_content = open_file.read()
            new_content = re.sub(find_regex, replace_regex, file_content)
            open_file.close()
            # Write new content in file
            open_file = open(file, "wt")
            open_file.write(new_content)
            open_file.close()
        except Exception as e:
            print("Error: "+e)
            try:
                open_file = open("../"+file, "rt")
            except:
                print(regex_file+" couldn't be opened")
                global failProject
                failProject = 1

    for file in laravelFiles:
        if regex_file is None:
            ChangeFile(file)
        else:
            if regex_file in file:
                ChangeFile(file)

    if failProject >= 1:
        raise TypeError(Style.RESET_ALL+'The file '+Fore.RED +
                        regex_file+Style.RESET_ALL+" couldn't be opened.")

# Generating Test List
def fetch_test_list(printTests=None, generateTests=None):
    current_row = 0
    # Laravel variables
    laravelFolders = [
        'app', 'app/Console', 'app/Events', 'app/Http/Controllers', 'app/Http/Middleware', 'app/Jobs', 'app/Notifications',
        'routes'
    ]
    laravelFiles = []
    controllerList = []
    jobsList = []
    notifyList = []
    middlewareList = []
    routeList = []
    # Loop through Laravel Folders and fetch php files if one of the above folders is used

    def LoopFolders(laravelFolders):
        for folder in laravelFolders:
            for currentpath, folders, files in os.walk(folder):
                if currentpath in laravelFolders:
                    for file in files:
                        if '.php' in str(file):
                            laravelFiles.append(os.path.join(currentpath, file))
    LoopFolders(laravelFolders)

    # If no folders are found, move up one parent
    if len(laravelFiles) == 0:
        newFolders = []
        for folder in laravelFolders:
            newFolders.append("../"+str(folder))
        LoopFolders(newFolders)

    # Generate the test lists
    def GenerateTest(file):
        def GenerateFileNameTest(file, testList):
            if generateTests == 1:
                generated_test = "Write a test for:" + \
                    str(file) + " in: " + str(file)
            else:
                generated_test = Style.RESET_ALL+"Write a test for: " + \
                    Fore.RED + str(file)+Style.RESET_ALL
            testList.append(generated_test)

        def GenerateFunctionTest(file, testList):
            f = open((file), 'r')
            x = 0
            for line in f:
                x = x + 1
                function = r"function.*\)"
                function_match = re.search(function, line)
                if function_match is not None:
                    print_match = function_match.group().replace('function', '')
                    if generateTests == 1:
                        generated_test = "Write a test for:" + \
                            print_match + " in: " + str(file) + ":" + str(x)
                    else:
                        generated_test = Style.RESET_ALL+"Write a test for:"+Fore.RED + print_match + \
                            Style.RESET_ALL+" in: " + Fore.RED + \
                            str(file)+":"+str(x)+Style.RESET_ALL
                    testList.append(generated_test)
            f.close()

        def GenerateRouteTest(file, testList):
            f = open((file), 'r')
            x = 0
            for line in f:
                x = x + 1
                route = r"Route::\w*\(.*@\w*\W*\)"
                route_match = re.search(route, line)
                if route_match is not None and '/_testing' not in str(route_match.group()):
                    print_match = route_match.group().replace('Route::', '')
                    if generateTests == 1:
                        generated_test = "Write a test for:" + \
                            print_match + " in: " + str(file) + ":" + str(x)
                    else:
                        generated_test = Style.RESET_ALL+"Write a test for:"+Fore.RED + print_match + \
                            Style.RESET_ALL+" in: " + Fore.RED + \
                            str(file)+":"+str(x)+Style.RESET_ALL
                    testList.append(generated_test)
            f.close()

        if any(re.findall(r'Controllers', str(file), re.IGNORECASE)):
            GenerateFunctionTest(file, controllerList)
        if any(re.findall(r'Jobs', str(file), re.IGNORECASE)):
            GenerateFunctionTest(file, jobsList)
        if any(re.findall(r'Notifications', str(file), re.IGNORECASE)):
            GenerateFileNameTest(file, notifyList)
        if any(re.findall(r'Middleware', str(file), re.IGNORECASE)):
            GenerateFileNameTest(file, middlewareList)
        if any(re.findall(r'routes', str(file), re.IGNORECASE)):
            GenerateRouteTest(file, routeList)

    for file in laravelFiles:
        GenerateTest(file)

    if printTests == 1:
        def PrintTests(title, testList):
            if len(testList) > 0:
                print(' ')
                print(str(title))
                print(' ')
                for test in testList:
                    print(test)
                print(' ')

        PrintTests('Controllers', controllerList)
        PrintTests('Jobs', jobsList)
        PrintTests('Notifications', notifyList)
        PrintTests('Middleware', middlewareList)
        PrintTests('Routes', routeList)

# -----------------------------------------------------------
# Start/End testing functions
# -----------------------------------------------------------

def step(describe):
    wait_ajax()
    global current_step
    global current_cmd
    global step_desc
    step_desc = describe
    current_cmd = current_cmd + 1
    if describe is not None:
        if shell is not None:
            browser.save_screenshot('pyrunner/'+str(current_cmd)+' - '+describe+'.png')
        print(Fore.CYAN+str(current_step)+': '+describe+Style.RESET_ALL)
        current_step = current_step + 1

def start(describe):
    wait_ajax()
    global current_step
    global current_test
    current_step = 1
    if describe is not None:
        current_test = describe
        if shell is not None:
            browser.save_screenshot('pyrunner/Test Start: '+str(describe)+'.png')
        print(' ')
        print(' ')
        print('────────────────────────────────────────────────────────────────────────────────────────────────────')
        print(' ')
        print('Starting: '+describe)
        print(' ')
        print('────────────────────────────────────────────────────────────────────────────────────────────────────')
        print(' ')


def end(describe):
    wait_ajax()
    if describe is not None:
        if shell is not None:
            browser.save_screenshot('pyrunner/Test End: '+str(describe)+'.png')
        print(Fore.GREEN+'')
        print(' ')
        print('----------------------------------------------------------------------------------------------------')
        print(' ')
        print(describe+': Succeeded')
        print(' ')
        print('----------------------------------------------------------------------------------------------------')
        print(Style.RESET_ALL+'')


def finished():
    print(Style.RESET_ALL+' ')
    print(' ')
    print(' ')
    print('Finished running PyRunner')
    print('Execution runtime: '+str(datetime.now()-test_time))
    print('All executions succeeded')
    print(' ')
    print(Style.RESET_ALL+' ')
    if dev == False:
        time.sleep(2)
        browser.quit()
    sys.exit(0)
    exit()


def failed(e):
        print(Style.RESET_ALL+' ')
        print('----------------------------------------------------------------------------------------------------')
        print(' ')
        print('Aborted executing due to fail')
        print('Execution runtime: '+str(datetime.now()-test_time))
        print(' ')
        print('----------------------------------------------------------------------------------------------------')
        print(' ')
        print(Fore.RED+'Failed at: '+str(current_test))
        print(Style.RESET_ALL+'Step '+str(current_step-1)+": "+str(step_desc))
        print(' ')
        print(str(e))
        print('')
        print(' ')
        browser.save_screenshot('pyrunner/failed_state.png')
        time.sleep(5)
        if shell is not None:
            import _db
            with ZipFile('pyrunner.zip', 'w') as zipObj:
            # Iterate over all the files in directory              
                for folderName, subfolders, filenames in os.walk('pyrunner'):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        if filename == 'database.txt':
                            zipObj.write(filePath, 'database/'+basename(filePath))
                        else:
                            zipObj.write(filePath, basename(filePath))
                for folderName, subfolders, filenames in os.walk('storage/logs'):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zipObj.write(filePath, 'logs/'+basename(filePath))
        if dev is None:
            browser.quit()
            sys.exit(1)
            exit()
