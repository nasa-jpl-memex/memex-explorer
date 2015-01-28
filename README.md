# memex-explorer-django
Memex explorer application re-written in Django 1.7

To setup the application, in an enviornment with Django 1.7 and Python 3 installed, run this command in the `memex_explorer` folder. This will create the database for the application using the migration scripts provided in the source code:
```
python manage.py migrate
```
Then, in the same folder run this command to launch the application as a local server:
```
python manage.py runserver
```
To set up superuser access to the administrative panel, run this command and provide a username, email, and password:
```
python manage.py createsuperuser
```
To make manual changes to the database, navigate to the following link and enter your username and password:
```
localhost:8000/admin
```
To make changes to scss stylesheets, do the following from the root of the repository, where config.rb is located:
```
$ gem install compass
$ compass watch

