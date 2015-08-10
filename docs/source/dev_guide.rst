###################################
Developer's Guide to Memex Explorer
###################################

*************************
Setting up Memex Explorer
*************************

To setup your machine, you will need Anaconda or Miniconda
installed. Miniconda is a minimal Anaconda installation that
bootstraps conda and Python on any operating system. Install `Anaconda
<http://continuum.io/downloads>`_ or `Miniconda
<http://conda.pydata.org/miniconda.html>`_ from their respective sites.

Memex Explorer requires conda, either from Miniconda or Anaconda.  

Application Setup
=================
    To set up a developer's environment, clone the repository, then
    run the app_setup.sh script:

    .. code-block:: html

	$ git clone https://github.com/memex-explorer/memex-explorer.git
	$ cd memex-explorer/source
	$ ./app_setup.sh

   You can then start the application from this directory:
	
    .. code-block:: html
	
	$ source activate memex
	$ supervisord

   Memex Explorer will now be running locally at `http://localhost:8000 <http://localhost:8000/>`_.

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
