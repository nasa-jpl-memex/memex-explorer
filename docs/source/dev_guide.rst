###################################
Developer's Guide to Memex Explorer
###################################

*************************
Setting up Memex Explorer
*************************

To setup your machine, you will need Anaconda or Miniconda installed. Miniconda is a minimal Anaconda installation that bootstraps conda and Python on any operating system. Install `Anaconda <http://continuum.io/downloads>`_ or `Miniconda <http://conda.pydata.org/miniconda.html>`_ from their respective sites.

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

Enabling Nutch Visualizations
=============================

   Nutch visualizations are not enabled by default. Nutch visualizations require RabbitMQ, and the method for installing RabbitMQ varies depending on the operating system. RabbitMQ can be installed via Homebrew on Mac, and apt-get on Debian systems. More information on how to install RabbitMQ, read `this page <https://www.rabbitmq.com/download.html>`_.

   To enable Bokeh visualizations for Nutch, change ``autostart=false`` to ``autostart=true`` for both of these directives in source/supervisord.conf, and then kill and restart supervisor.

   .. code-block:: html

      [program:rabbitmq]
      command=rabbitmq-server
      priority=1
      -autostart=false
      +autostart=true

      [program:bokeh-server]
      command=bokeh-server --backend memory --port 5006
      priority=1
      -autostart=false
      +autostart=true

Tests
=====
    To run the tests, return to the root directory and run:

    .. code-block:: html

       $ py.test

The Database Model
==================
The current entity relation diagram:

.. image:: _static/img/DbVisualizer.png

Updating the Database
---------------------
As of version 0.4.0, Memex Explorer will start tracking all database migrations. This means that you will be able to upgrade your databse and preserve the data without any issues.

If you are using a version that is 0.3.0 or earlier, and you are unable to update your database without server errors, the best course if action is to delete the existing `file at source/db.sqlite3` and start over with a fresh database.
