[![Build
Status](https://travis-ci.org/ContinuumIO/blaze.png)](https://travis-ci.org/ContinuumIO/blaze)
[![Coverage Status](https://coveralls.io/repos/ContinuumIO/memex-explorer/badge.svg?branch=memex-django)](https://coveralls.io/r/ContinuumIO/memex-explorer?branch=memex-django)

# memex-explorer-django
Memex explorer application re-written in Django 1.7
* To setup the environment, do the following:
```
$ wget http://bit.ly/miniconda
$ bash Miniconda-latest-Linux-x86_64.sh
$ bash install.sh
$ conda env create -n memex -f environment.yml
$ source activate memex
```
* To setup the application, in an environment with Django 1.7 and Python 3 installed, run this command in the `memex_explorer` folder. This will create the database for the application using the migration scripts provided in the source code:
```
$ cd memex_explorer
$ python manage.py migrate
```
* Then, in the same folder run this command to launch the application as a local server:
```
$ python manage.py runserver
```
* To set up superuser access to the administrative panel, run this command and provide a username, email, and password:
```
$ python manage.py createsuperuser
```
* To access the administration panel navigate to http://localhost:8000/admin after running `python manage.py runserver`. Here you will be able to view and make manual changes to the database.
* To run the tests, run the command:
```
$ py.test
```
# Installing Compass
If you need to make changes to the .scss stylesheets, [Compass](http://compass-style.org/) is a useful tool. The following are instructions on how to install compass without using `sudo`.
* For mac users, add this line to your `~/.bash_profile`:
```
export PATH=/Users/<username>/.gem/ruby/<ruby version>/bin:$PATH
```
Then run `$ gem install compass --user-install`. This will install Compass on your system.
* To make changes to the stylesheets, do:
```
$ cd ../
$ compass watch
```
