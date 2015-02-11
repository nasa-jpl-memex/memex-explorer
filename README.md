[![Build
Status](https://travis-ci.org/ContinuumIO/blaze.png)](https://travis-ci.org/ContinuumIO/blaze)
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
* To make changes to scss stylesheets, do the following from the root of the repository, where config.rb is located:
```
$ cd ../
$ gem install compass
$ compass watch
```
