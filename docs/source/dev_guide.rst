###################################
Developer's Guide to Memex Explorer
###################################

*************************
Setting up Memex Explorer
*************************

Environment
===========
    To setup the environment, do the following:

    .. code-block:: html

        $ http://bit.ly/miniconda
        $ bash miniconda
        $ conda env create -n memex -f environment.yml
        $ source activate memex

Application Setup
=================
    To setup the application, in an environment with Django 1.7 and Python <2.6 installed, run these commands in the source folder. This will create the database for the application using the migration scripts provided in the source code:

    .. code-block:: html

        $ cd source
        $ python manage.py migrate

    Then, in the same folder run this command to launch the application as a local server:

    .. code-block:: html

        $ python manage.py runserver

    To set up superuser access to the administrative panel, run this command and provide a username, email, and password:

    .. code-block:: html

        $ python manage.py createsuperuser

    To access the administration panel navigate to http://localhost:8000/admin after running python manage.py runserver. Here you will be able to view and make manual changes to the database.

Tests
=====
    To run the tests, return to the root directory and run:

    .. code-block:: html

        $ py.test

******************
Installing Compass
******************
    If you need to make changes to the .scss stylesheets, `Compass <http://compass-style.org/>`_ is a useful tool. The following are instructions on how to install compass without using sudo.

    For mac users, add this line to your ~/.bash_profile:

    .. code-block:: html

        export PATH=/Users/<username>/.gem/ruby/<ruby version>/bin:$PATH

    Then run $ gem install compass --user-install. This will install Compass on your system.

    To make changes to the stylesheets, do:

    .. code-block:: html

        $ cd ../
        $ compass watch

******************
The Database Model
******************
The current entity relation diagram:

.. image:: _static/img/DbVisualizer.png
