This project was created to test VeeaHub Enrollment flow using as framework [RobotFramework](https://robotframework.org/) and [python](https://www.python.org/) 

The flow requires the following projects running in the local machine:
- [Enrollment-Service](https://github.com/Max2Inc/enrollment-service)
- [Activation&Configuration-Service](https://github.com/Max2Inc/activation-configuration)
- [Bootstrap-Service](https://github.com/Max2Inc/bootstrap-service)
- [Certificate-Service](https://github.com/Max2Inc/certificate-service)
- [Billing-Service](https://github.com/Max2Inc/billing-service)
- [Key-cloak](https://www.keycloak.org/) It is used as the authentication service

In order to know about the services you can contact with [Veeahub team](https://www.veea.com/support/veeahub/)

The enrollment-flow have the following basic endpoints:
- Veea Hub Enrollment with Basic package by default.
- Veea Hub Upgrade with Premium package
- Veea Hub Downgrade to Basic package
- Get Mesh configuration status to get the Veea Hub progress

Currently, there are test-cases to test some flows, the implementation is progress.

## Steps to execute the test-cases
#### Install Virtual environment
~~~
$ sudo apt-get install python3-venv
~~~

#### Create a Virtual environment in your project
It should use the command `venv`, example: `$ venv {envName}`
~~~
$ python3 -m venv venv
~~~
After that you can use the command `$ which python` to display the location of your Python interpreter.

#### Activating the Virtual environment
~~~
$ source venv/bin/activate
~~~
We can use the command `$ deactivate` in order to leave the environment.
#### Install package from requirements file
~~~
$ python -m pip install -r requirements.txt
~~~

## How execute test
~~~
$ cd vh-automation
$ robot test/enrollment_veeahub.robot
$ robot test/unrollment_veeahub.robot
~~~

Another commands utils
#### Export a list of all installed packages
~~~
$ python -m pip freeze > requirements.txt
~~~