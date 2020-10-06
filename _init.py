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
import chromedriver_py as chromedriver
from chromedriver_py import binary_path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from xlwt import Workbook

init()

shutil.rmtree('pyrunner', ignore_errors=True)
os.system('mkdir pyrunner')

# -----------------------------------------------------------
# Set Up Browser
# -----------------------------------------------------------

def FindString(key,content):
    regex = r""+key+"=.*"
    match = re.search(regex, content)
    match = match.group()
    match = match.replace(key+'=','')
    return match

# Get from .env
f = open(('.env'), 'r')
env = f.read()
APP_URL = FindString("APP_URL",env)

customArgs = []
customArgs.append('--dev')
customArgs.append('--debug')
customArgs.append('--shell')
customArgs.append('--cicd')
customArgs.append('--screenshots')

dev = None
shell = None
debug = None
cicd = None
screenshots = None

max_retries = 1
max_clicks = 1
implicitWait = 10

for customArg in customArgs:
    for sysArg in sys.argv: 
        if sysArg == '--dev':
            dev = True
        if sysArg == '--shell':
            shell = True
        if sysArg == '--debug':
            debug = True
        if sysArg == '--cicd':
            cicd = True
        if sysArg == '--screenshots':
            screenshots = True

if shell is not None:
    print('Executing PyRunner in shell')
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
else:
    print('Executing PyRunner')
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--auto-open-devtools-for-tabs')
    
if cicd is not None:
    max_retries = 2
    max_clicks = 1
    implicitWait = 30
    
try:
    browser = webdriver.Chrome(executable_path=binary_path,options=options)
except Exception as e:
    print(' ')
    print('PyRunner couldn\'t launch Google Chrome. Make sure your chrome version and chromedriver use the same version.')
    print(' ')
    print(str(e))
    print(' ')
    print('To install the correct chromedriver version: ')
    print("pip install --pre 'chromedriver-py==VERSION.*' --force-reinstall")
    exit()
browser.implicitly_wait(1)
browser.get('http://localhost')
browser.maximize_window()
current_url = browser.current_url

# -----------------------------------------------------------
# Functions which execute browser commands
# -----------------------------------------------------------
    
current_step = 0
describe = None
test_time=datetime.now()
failProject = None
step_desc = None
current_test = None
current_url = None

def wait_document(timeout=20):
    wait = WebDriverWait(browser, timeout)
    try:
        wait.until(lambda browser: browser.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass
    
def wait_ajax(timeout=30):
    wait = WebDriverWait(browser, timeout)
    try:
        wait.until(lambda browser: browser.execute_script('return jQuery.active') == 0)
        wait.until(lambda browser: browser.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass
    
def get(url=''):
    wait_document(20)
    browser.get(url)

@retry(stop_max_attempt_number=max_clicks)
def click(xpath=None, css=None, id=None, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(10)
    def Click(css, xpath, id):
        if css is not None:
            try:
                if debug is not None:
                    print('Trying to click with CSS & Selenium on: '+str(css))
                browser.find_element_by_css_selector(css).click()
                if debug is not None:
                    print(Fore.GREEN+'Clicked with css, returning'+Style.RESET_ALL)
                return
            except:
                try:
                    if debug is not None:
                        print('Trying to click with first CSS result & JS on: '+str(css))
                    browser.execute_script('document.querySelectorAll("'+css+'")[0].click()')
                    if debug is not None:
                        print(Fore.GREEN+'Clicked with css, returning'+Style.RESET_ALL)
                    return
                except:
                    if debug is not None:
                        print(Fore.RED+'CSS click failed with: ' + str(css)+Style.RESET_ALL)
                    try:
                        if debug is not None:
                            print('Trying to click with CSS & JS on: '+str(css))
                        browser.execute_script('document.querySelectorAll("'+css+'").click()')
                        if debug is not None:
                            print(Fore.GREEN+'Clicked with css, returning'+Style.RESET_ALL)
                        return
                    except:
                        if debug is not None:
                            print(Fore.RED+'CSS click failed with: ' + str(css)+Style.RESET_ALL)
        if xpath is not None:
            try:
                if debug is not None:
                    print('Trying to click with Xpath on: '+str(xpath))
                browser.find_element_by_xpath(xpath).click()
                if debug is not None:
                    print(Fore.GREEN+'Clicked with Xpath, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print(Fore.RED+'Xpath click failed with: ' + str(xpath)+Style.RESET_ALL)
                if id is None:
                    raise TypeError("Can't click this element: "+str(xpath)+".")
            try:
                if debug is not None:
                    print('Trying to click with Xpath & JS on: '+str(xpath))
                browser.execute_script("document.evaluate('"+str(xpath)+"', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
                if debug is not None:
                    print(Fore.GREEN+'Clicked with Xpath, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print(Fore.RED+'Xpath click failed with: ' + str(xpath)+Style.RESET_ALL)
        if id is not None:
            try:
                if debug is not None:
                    print('Trying to click with ID & JS: '+"document.getElementById('"+id+"').click()")
                browser.execute_script("document.getElementById('"+id+"').click()")
                if debug is not None:
                    print(Fore.GREEN+'Clicked with browser script, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print(Fore.RED+'ID click failed with: ' + str(id)+Style.RESET_ALL)
            try:
                if debug is not None:
                    print('Trying to click with ID on: '+'//*[@id="'+id+'"]')
                browser.find_element_by_xpath('//*[@id="'+id+'"]').click()
                if debug is not None:
                    print(Fore.GREEN+'Clicked with ID, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print(Fore.RED+'ID click failed with: ' + str(id)+Style.RESET_ALL)
            try:
                if debug is not None:
                    print('Trying to click with ID on: '+str(id))
                browser.find_element_by_id(id).click()
                if debug is not None:
                    print(Fore.GREEN+'Clicked with ID, returning'+Style.RESET_ALL)
                return
            except:
                if debug is not None:
                    print(Fore.RED+'ID click failed with: ' + str(id)+Style.RESET_ALL)
                raise TypeError("Can't click this element: "+str(id)+".")
    Click(css, xpath, id)

@retry(stop_max_attempt_number=max_retries)
def select2(selector=None, cmd=None, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    try:
        if selector is not None and cmd is not None:
            print('Trying to execute command on select2 element(s): '+str(selector))
            browser.execute_script("$('"+str(selector)+"').select2('"+str(cmd)+"')")
        if selector is not None and cmd is not None:
            print(Fore.GREEN+'Select2 ('+str(cmd)+') has been executed'+Style.RESET_ALL)
        return
    except:
        if selector is not None and cmd is not None:
            print(Fore.RED+'Select2 cmd execution failed: ' + str(selector)+Style.RESET_ALL)
        time.sleep(1)
        raise TypeError("Can't execute select2 ("+str(cmd)+") on: "+str(selector)+".")
    
@retry(stop_max_attempt_number=max_retries)
def hover(selector=None, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    try:
        if selector is not None:
            print('Trying to hover on: '+str(selector))
            element = browser.find_element_by_css_selector(selector)
            hover = ActionChains(browser).move_to_element(element)
            hover.perform()
        return
    except:
        if selector is not None:
            print(Fore.RED+'Hovering failed on: ' + str(selector)+Style.RESET_ALL)
        print("Can't hover on: "+str(selector)+".")
    time.sleep(1.5)

@retry(stop_max_attempt_number=max_retries)
def scroll_to(selector=None, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    try:
        if selector is not None:
            print('Trying to scroll to: '+str(selector))
            element = browser.find_element_by_css_selector(selector)
            scroll = ActionChains(browser).move_to_element(element)
            scroll.perform()
        return
    except:
        if selector is not None:
            print(Fore.RED+'Scrolling failed to: ' + str(selector)+Style.RESET_ALL)
        print("Can't scroll to: "+str(selector)+".")

@retry(stop_max_attempt_number=max_retries)
def switch_tab(index):
    wait_document()
    browser.switch_to.window(browser.window_handles[index])

# Selecting

@retry(stop_max_attempt_number=max_retries)
def select_value_name(name, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Selecting '+str(value)+' in '+str(name))
    browser.find_element_by_xpath(
        "//select[@name='"+name+"']/option[@value='"+value+"']").click()

@retry(stop_max_attempt_number=max_retries)
def select_index_name(name, index, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Selecting '+str(index)+' in '+str(name))
    browser.find_element_by_xpath(
        "//select[@name='"+name+"']/option["+index+"]").click()
    
@retry(stop_max_attempt_number=max_retries)
def select_value_id(id, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Selecting '+str(value)+' in '+str(id))
    browser.find_element_by_xpath(
        "//select[@id='"+id+"']/option[@value='"+value+"']").click()

@retry(stop_max_attempt_number=max_retries)
def select_index_id(id, index, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Selecting '+str(index)+' in '+str(id))
    browser.find_element_by_xpath(
        "//select[@id='"+id+"']/option["+index+"]").click()
    
@retry(stop_max_attempt_number=max_retries)
def find_text(text, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to find text: '+str(text))
    element = browser.find_element_by_xpath(
        "//*[contains(text(), '"+text+"')]")
    if element.is_displayed() is False:
        return False

@retry(stop_max_attempt_number=max_retries)
def find_id(id, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to find ID: '+str(id))
    element = browser.find_element_by_id(id)
    if element.is_displayed() is True:
        print('Found ID: '+id)
    else:
        return False

@retry(stop_max_attempt_number=max_retries)
def find_class(el_class, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to find class: '+str(el_class))
    element = browser.find_element_by_class_name(el_class)
    @retry(stop_max_attempt_number=timeout)
    def Visible():
        if element.is_displayed() is True:
            if debug is not None:
                print('Found class: '+el_class)
        else:
            time.sleep(1)
            raise TypeError('This element was found but not visible: '+el_class)
    Visible()

@retry(stop_max_attempt_number=max_retries)
def find_css(css, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to find css: '+str(css))
    element = browser.find_element_by_css_selector(css)
    @retry(stop_max_attempt_number=timeout)
    def Visible():
        if element.is_displayed() is True:
            if debug is not None:
                print('Found CSS: '+css)
        else:
            time.sleep(1)
            raise TypeError('This element was found but not visible: '+css)
    Visible()

@retry(stop_max_attempt_number=max_retries)
def find_name(name, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to find name: '+str(name))
    element = browser.find_element_by_name(name)
    @retry(stop_max_attempt_number=timeout)
    def Visible():
        if element.is_displayed() is True:
            if debug is not None:
                print('Found name: '+name)
        else:
            time.sleep(1)
            raise TypeError('This element was found but not visible: '+name)
    Visible()
    
@retry(stop_max_attempt_number=max_retries)
def find_xpath(xpath, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to find Xpath: '+str(xpath))
    element = browser.find_element_by_xpath(xpath)
    @retry(stop_max_attempt_number=timeout)
    def Visible():
        if element.is_displayed() is True:
            if debug is not None:
                print('Found Xpath: '+xpath)
        else:
            time.sleep(1)
            raise TypeError('This element was found but not visible: '+xpath)
    Visible()

# Typing

@retry(stop_max_attempt_number=max_retries)
def type_xpath(xpath, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
            print('Trying to type: '+str(value)+' in '+str(xpath))
    browser.find_element_by_xpath(xpath).send_keys(value)


@retry(stop_max_attempt_number=max_retries)
def type_name(name, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(name))
    browser.find_element_by_name(name).send_keys(value)


@retry(stop_max_attempt_number=max_retries)
def type_id(id, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(id))
    browser.find_element_by_id(id).send_keys(value)


@retry(stop_max_attempt_number=max_retries)
def type_css(css, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(css))
    browser.find_element_by_css_selector(css).send_keys(value)
    
# Clearing and Typing
@retry(stop_max_attempt_number=max_retries)
def change_text_xpath(xpath, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(xpath))
    browser.find_element_by_xpath(xpath).clear()
    browser.find_element_by_xpath(xpath).send_keys(value)
    
@retry(stop_max_attempt_number=max_retries)
def change_text_name(name, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(name))
    browser.find_element_by_name(name).clear()
    browser.find_element_by_name(name).send_keys(value)
    
@retry(stop_max_attempt_number=max_retries)
def change_text_id(id, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        print('Trying to type: '+str(value)+' in '+str(id))
    browser.find_element_by_id(id).clear()
    browser.find_element_by_id(id).send_keys(value)
    
@retry(stop_max_attempt_number=max_retries)
def change_text_css(css, value, timeout = implicitWait):
    wait_document()
    browser.implicitly_wait(timeout)
    if debug is not None:
        browser.find_element_by_css_selector(css).clear()
        browser.find_element_by_css_selector(css).send_keys(value)
    
@retry(stop_max_attempt_number=max_retries)
def type_tinymce(selector, value):
    wait_document()
    value = value.replace('\n',' ')
    if debug is not None:
        print('Trying to type: '+str(value)+' in TinyMCE with selector: '+str(selector))
    print("tinymce.get(\""+str(selector)+"\").setContent(\""+str(value)+"\", {format: \"raw\"});")
    browser.execute_script("tinymce.get(\""+str(selector)+"\").setContent(\""+str(value)+"\", {format: \"raw\"});")


# -----------------------------------------------------------
# Code refactoring
# -----------------------------------------------------------

def scan_regex(regex):
    # Laravel variables
    laravelFolders = [
        'app', 'bootstrap', 'config', 'database', 'public', 'resources', 'routes', 'modules'
    ]
    laravelFiles = []
    failProject = 0

    def LoopFolders(laravelFolders):
        for folder in laravelFolders:
            for currentpath, folders, files in os.walk(folder):
                for file in files:
                    if '.php' in str(file) and 'vendor' not in str(currentpath):
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
    global current_step
    global current_url
    global step_desc
    if browser.current_url != current_url:
        wait_ajax(5)
    current_url = browser.current_url
    wait_document()
    wait_ajax(2)
    step_desc = describe
    if describe is not None:
        if screenshots is not None:
            browser.save_screenshot('pyrunner/'+str(current_step)+' - '+describe+'.png')
        if debug is not None:
            print(Fore.CYAN+str(current_step)+': '+describe+Style.RESET_ALL)
        current_step = current_step + 1

def start(describe):
    wait_document()
    global current_step
    global current_test
    if describe is not None:
        current_test = describe
        print(' ')
        print(' ')
        print('────────────────────────────────────────────────────────────────────────────────────────────────────')
        print(' ')
        print('Starting: '+describe)
        print(' ')
        print('────────────────────────────────────────────────────────────────────────────────────────────────────')
        print(' ')


def end(describe):
    wait_document()
    if describe is not None:
        print(Fore.GREEN+'')
        print(' ')
        print('----------------------------------------------------------------------------------------------------')
        print(' ')
        print(describe+': Succeeded')
        print(' ')
        print('----------------------------------------------------------------------------------------------------')
        print(Style.RESET_ALL+'')


def finished(group=None):
    print(Style.RESET_ALL+' ')
    print(' ')
    print(' ')
    if group is None:
        print(Fore.GREEN+'Finished running PyRunner'+Style.RESET_ALL)
    else :
        print(Fore.GREEN+'Finished running Group '+str(group)+Style.RESET_ALL)
    print('Execution runtime: '+str(datetime.now()-test_time))
    print('All executions succeeded')
    print(' ')
    print(Style.RESET_ALL+' ')
    if dev == False:
        time.sleep(2)
        browser.quit()
    sys.exit(0)
    exit()


def failed(failedTests):
        print(Style.RESET_ALL+' ')
        print('----------------------------------------------------------------------------------------------------')
        print(' ')
        print('Aborted executing due to fail')
        print('Execution runtime: '+str(datetime.now()-test_time))
        print(' ')
        print('----------------------------------------------------------------------------------------------------')
        for failed in failedTests:
            print(' ')
            print(Style.RESET_ALL+'Failed test at step '+str(failed['step'])+': '+Fore.RED+str(failed['name'])+Style.RESET_ALL)
            print(Style.RESET_ALL+'Error: '+Fore.RED+str(failed['error'])+Style.RESET_ALL)
            print(' ')
        print(' ')
        time.sleep(5)
        if cicd is not None:
            try:
                with ZipFile('pyrunner.zip', 'w') as zipObj:
                # Iterate over all the files in directory              
                    for folderName, subfolders, filenames in os.walk('pyrunner'):
                        for filename in filenames:
                            filePath = os.path.join(folderName, filename)
                            if filename == 'database.txt':
                                try:
                                    zipObj.write(filePath, 'database/'+basename(filePath))
                                except Exception as e:
                                    print(e)
                            else:
                                try:
                                    zipObj.write(filePath, basename(filePath))
                                except Exception as e:
                                    print(e)
                    for folderName, subfolders, filenames in os.walk('storage/logs'):
                        for filename in filenames:
                            try:
                                filePath = os.path.join(folderName, filename)
                                zipObj.write(filePath, 'logs/'+basename(filePath))
                            except Exception as e:
                                print(e)
            except Exception as e:
                print(e)
        if dev is None:
            browser.quit()
            sys.exit(1)
            exit()
