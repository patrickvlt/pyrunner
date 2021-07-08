![image](https://user-images.githubusercontent.com/43636101/124980975-4fb3bd00-e035-11eb-9c40-aa8737b9d60c.png)


## About PyRunner

Pyrunner is a python package, which can run browser tests for Laravel applications. Pyrunner currently features:

- Interactively develop browser tests with the development mode
- Log and make screenshots of each step
- Retry failed test automatically as many times as you want
- Easy to use in CICD, less prone to crashes than Laravel Dusk

# Usage

Install Python: https://www.python.org/downloads/release/python-381/

Install Pip: https://pip.pypa.io/en/stable/installing/


Go to the root of your project.

Install this package:

```
composer require pveltrop/pyrunner:dev-master#(commit)
```

Then install PyRunner in your Laravel project:
```
php artisan pyrunner:install
```

Prepare your (test) database:

```
php artisan migrate:fresh --seed (--database=mysql_testing)
```

Launch PyRunner in a new terminal:
```
php artisan pyrunner:start (--dev) (--debug) (--shell) (--screenshots)
```

Launch PyRunner in your active terminal:
```
python vendor/pveltrop/pyrunner/test_app.py (--dev) (--debug) (--shell) (--screenshots)
```

## Parameters

<h4>Development (--dev)</h4>

```
php artisan pyrunner:start --dev
```

Launches the app and inserts a breakpoint. Meaning you get an interactive terminal, so you can test browser commands, or run a test individually.

Keep in mind:

Development mode will insert a breakpoint at launch, so you can run whatever you want in your _tests.py file.
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
ipdb> reload(tests)
```
This will reload your _tests.py file.
Then:
```
ipdb> tests.nameoftest()
```

<h4>Debug (--debug)</h4>

```
php artisan pyrunner:start --debug
```

This option will enable more specific output during test command executions. This can be helpful to pinpoint where PyRunner is struggling.

<h4>Screenshots (--screenshots)</h4>

```
php artisan pyrunner:start --screenshots
```

This option will enable screenshots. Screenshots will be made whenever you define a new step (pr.step()).

# ENV

```
php artisan pyrunner:env
```

This option will generate a .env.example and .env.testing. Change values you want or dont want in version control.

### Configure for Laravel

Make sure your APP_URL is set correctly, to the same address as you use locally.

- Make a .env.testing file, for local and GitLab testing, if you skipped this step during php artisan pyrunner:install

```
php artisan pyrunner:env
```

If this environment doesn't work locally, it won't work on GitLab either.

- IMPORTANT: set TELESCOPE_ENABLED=false, otherwise migrations wont work currently

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

# Writing tests

- Define test functions in _tests.py (in your project root) with this structure:

```

# -----------------------------------------------------------
# Tests
# -----------------------------------------------------------
        
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

## Selecting

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

# Docker Image

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
