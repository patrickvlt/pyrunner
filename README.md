# Usage

Download Python: https://www.python.org/downloads/release/python-381/

Download Pip: https://pip.pypa.io/en/stable/installing/


Go to the root of your project.

Install latest requirements, chromedriver might have been adjusted due to delayed releases:

```
pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt
```

Prepare your (test) database:

```
php artisan migrate:fresh --seed --database=mysql_testing
```

Serve your project:

```
php artisan serve --port=80 --host=localhost --env=testing
```

Run your tests: 

```
python vendor/pveltrop/pyrunner/test_app.py
```

## dev Parameter

```
python vendor/pveltrop/pyrunner/test_app.py dev
```

Launches the app and inserts a breakpoint. Meaning you get an interactive terminal, so you can test browser commands, or run a test individually.

Keep in mind:

```
python vendor/pveltrop/pyrunner/test_app.py dev
```
Will launch dev mode with a breakpoint, the terminal will show:
```
ipdb>
```
So if you want to run the fake function in _tests.py, you run fake().name() (for example):
```
ipdb> fake.email()
'siennaschiffer@van.com'
```


If you want to run all tests, and insert a breakpoint if it fails anywhere (your test code will be reloaded every time):
```
ipdb> RunTests()
```

If you want to re-run a single test, first literally enter:
```
ipdb> reload(test)
```
Then:
```
ipdb> test.nameoftest()
```

## Other parameters


```
python vendor/pveltrop/pyrunner/test_app.py dev debug
```

Shows more information during the execution of a browser command.

```
python vendor/pveltrop/pyrunner/test_app.py debug shell
```

This runs the tests in a terminal only. You won't see the browser.

# Test Commands

```
pr.click(xpath,css,id)
```

The parameters are selectors for HTML elements. (right click in Chrome/Firefox)
All three are optional, but the more you use, the more likely the click will succeed.

```
pr.switch_tab(index)
```

Switch the browser to the provided index.

```
pr.select_value_name(name, value)
```

Select an option in an HTML element, by value.

```
pr.select_index_name(name, index)
```

Select an option in an HTML element, by index.

```
pr.select_value_id(id, value)
```

Select an option in an HTML element, by value.

```
pr.select_index_id(id, index)
```

Select an option in an HTML element, by value.

```
pr.find_text(text)
```

Find text on the current page.

```
pr.find_id(id)
```

Try to find a VISIBLE element by ID.

```
pr.find_class(class)
```

Try to find a VISIBLE element by Class.

```
pr.find_css(css)
```

Try to find a VISIBLE element by CSS selector.

```
pr.find_name(name)
```

Try to find a VISIBLE element by Name.

```
pr.find_xpath(xpath)
```

Try to find a VISIBLE element by Xpath.

## Typing

```
pr.type_xpath(xpath)
```

Try to type in an element selected by xpath.

```
pr.type_name(name)
```

Try to type in an element selected by name.

```
pr.type_id(id)
```

Try to type in an element selected by id.

```
pr.type_css(css)
```

Try to type in an element selected by css.

```
pr.change_text_xpath(xpath)
```

Try to clear and type text in an element selected by xpath.

```
pr.change_text_name(name)
```

Try to clear and type text in an element selected by name.

```
pr.change_text_id(id)
```

Try to clear and type text in an element selected by id.

```
pr.change_text_css(css)
```

Try to clear and type text in an element selected by css.

# Installation

### Preparing the Docker image

- Build a docker image for your project

```
- Navigate to the Docker folder in this repo
- Copy and paste the following files from your project to this folder, to speed up CI/CD:
composer.json
composer.lock
package.json
package-lock.json
- docker login registry.gitlab.com
- docker build -t registry.gitlab.com/(group)/(repository) .
- docker push registry.gitlab.com/(group)/(repository)
```

- Update the Docker image being used in .gitlab-ci.yml

### Installing and preparing PyRunner in your project
- Open your website's project root folder

```
composer require pveltrop/pyrunner
```

```
pip install -r https://raw.githubusercontent.com/43874/pyrunner/master/requirements/requirements.txt
```

- Go to vendor/pveltrop/pyrunner
- Copy _tests_example.py to your project root / and name it _tests.py

- Define test functions with this structure:

```

# -----------------------------------------------------------
# Tests
# -----------------------------------------------------------
        
@pr.retry(stop_max_attempt_number=max_test_retries)
def users_can_login():
    pr.start('Users Can Login') # Prints start of test
    pr.step('Logout first') # Prints current step being executed
    pr.browser.get('http://localhost/_testing/pylogout') # Redirecting browser
    pr.step('Enter email') 
    pr.type_xpath('//*[@id="email"]', pyUserEmail) # Typing in a field
    pr.step('Enter password') 
    pr.type_xpath('//*[@id="password"]', pyUserPassword)
    pr.step('Login') 
    pr.click('//*[@id="kt_login_signin_submit"]','#kt_login_signin_submit','kt_login_signin_submit') # Click function has 3 parameters. The order is: Xpath selector, CSS selector, ID selector. Send atleast one.
    pr.end('Users Can Login') # Prints end of test
    
# -----------------------------------------------------------
# End of tests
# -----------------------------------------------------------

```

- Define refactoring functions with this structure:

```

# -----------------------------------------------------------
# Refactoring/scanning
# -----------------------------------------------------------

def scan_for_dd():
    pr.start('Check if all dd() is removed from code')
    pr.step('Scan files with RegEx')
    pr.scan_regex(r"dd\([\',\"].*[\',\"]\)")
    pr.end('Check if all dd() is removed from code')
    
# -----------------------------------------------------------
# End of refactoring
# -----------------------------------------------------------

```

Use a localhost URL in your tests, as shown above in the examples. 
The testcontainer on GitLab will only use localhost, NOT a URL defined in a hostfile 
Summarized:
http://www.projectname.test/ will not work. 
http://localhost/ will work.

### Configure for Laravel

- Make a .env.testing file, for local and GitLab testing
If this environment doesn't work locally, it won't work on GitLab either.
- Go to config/database.php, copy the mysql array and name it mysql_testing. Change DB_DATABASE to TESTING_DB_DATABASE in mysql_testing
- To migrate the test DB locally: 
```
php artisan migrate:fresh --seed --database=mysql_testing
```
- Define TESTING_DB_DATABASE in your local, testing and example env.
- Make sure your .env.testing isnt in production mode, production mode will halt artisan commands with interactions!
- IMPORTANT: set TELESCOPE_ENABLED=false, otherwise migrations wont work currently

### Launching tests
- Serve your project on localhost:80 with a testing .env, you can do this with:
```
php artisan serve --port=80 --host=localhost --env=testing
```

- To start testing your project:

```
python vendor/pveltrop/pyrunner/test_app.py
```

### GitLab CI/CD file

- Add the testing database name to the variables of .gitlab-ci.yml:

```
variables:
  MYSQL_DATABASE: (database_name)
```

### Optional if you want to receive testresults in Slack or Pushbullet:

- On GitLab, go to Settings -> CI/CD -> Variables
- Define a SLACK variable which is the url for the webhook you want to use
- Define a PUSHBULLET variable which contains the API key of your Pushbullet account
- For pushbullet: also pass a GitLab variable in the yml file with parameter: --pbchannel=channelName

### Optional if you want to host a GitLab runner yourself:

- Install GitLab runner on a pc and link it to your project repository in CI/CD 
- Install docker on this PC, and pull the image you built earlier:
```
docker pull registry.gitlab.com/(group)/(repository)
```
