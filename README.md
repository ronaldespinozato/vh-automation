## Install Virtual environment
~~~
$ sudo apt-get install python3-venv
~~~

## Create a Virtual environment in your project
~~~
$ python3 -m venv env
~~~
After that you can use the command `$ which python` to display the location of your Python interpreter.

## Activating the Virtual environment
~~~
$ source env/bin/activate
~~~

## Leave, exist, deactivate virtual env
~~~
$ deactivate
~~~

## Install package from requirements file
~~~
$ python -m pip install -r requirements.txt
~~~

## How execute test
~~~
$ cd vh-automation
$ robot ./test/enrollment_veeahub.robot
~~~

## Export a list of all installed packages
~~~
$ python -m pip freeze > requirements.txt
~~~

## Install Roboframework
~~~
$ pip install robotframework
~~~