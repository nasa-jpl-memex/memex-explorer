[![Build Status](https://travis-ci.org/memex-explorer/memex-explorer.svg?branch=master)](https://travis-ci.org/memex-explorer/memex-explorer)
[![Coverage Status](https://coveralls.io/repos/ContinuumIO/memex-explorer/badge.svg?branch=master)](https://coveralls.io/r/ContinuumIO/memex-explorer?branch=master)

# *DISCLAIMER*

*Memex explorer has currently been put on hold. Support and development on this project has ceased for the immediate future.*

# memex-explorer

Memex Explorer is a web application that provides easy-to-use interfaces for gathering, analyzing, and graphing web crawl data.

# Local Development
To setup your machine, you will need Anaconda or Miniconda installed. Miniconda is a minimal Anaconda installation that bootstraps conda and Python on any operating system. Install Anaconda from http://continuum.io/downloads or Miniconda from http://conda.pydata.org/miniconda.html

Clone the repository, then:

```bash
cd memex-explorer/source
```

Run the following commands:

```bash
$ ./app_setup.sh
$ source activate memex
$ supervisord
```

This script will set up a conda environment named memex, prepare the application by creating an empty database, then launch all of the necessary services for the application. If there are any problems with any of these commands, please report them as a [GitHub issue](https://github.com/memex-explorer/memex-explorer/issues).

If you have already run the install script, simply run `supervisord` from the `memex-explorer/source` directory to restart all of the services.

The supervisord will start supervisord in the foreground, which will in turn ensure that all services associated with the core Memex Explorer environment are running.  To stop supervisord and the associated services, send an interrupt to the process with `Ctrl-c`.

**Memex Explorer will now be running locally at http://localhost:8000**

# Testing

To run memex-explorer tests, use the following command from within an active environment:

```
$ py.test
```

# Building the Documentation
The project documentation is written in [reStructuredText](http://docutils.sf.net/rst.html) and can be built using [Sphinx](http://sphinx-doc.org/).

```
$ cd docs
$ make html
```

The documentation is then available within `build/html/index.html`

# Administration

To access the administration panel, navigate to http://localhost:8000/admin (or the equivalent deployed URL) after starting Memex Explorer. Here you will be able to view and make manual changes to the database.

