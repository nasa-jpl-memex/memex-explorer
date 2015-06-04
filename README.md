[![Build Status](https://travis-ci.org/memex-explorer/memex-explorer.svg?branch=master)](https://travis-ci.org/memex-explorer/memex-explorer)
[![Coverage Status](https://coveralls.io/repos/ContinuumIO/memex-explorer/badge.svg?branch=memex-django)](https://coveralls.io/r/ContinuumIO/memex-explorer?branch=memex-django)

# memex-explorer

Memex Explorer is a web application that provides easy-to-use interfaces for gathering, analyzing, and graphing web crawl data.

# Local Development

The current recommended method for developing Memex Explorer locally is to run it in a [Vagrant](https://www.vagrantup.com/) environment using [VirtualBox](http://docs.vagrantup.com/v2/virtualbox).  After you have installed Vagrant and VirtualBox, run the following commands.

```
$ git clone https://github.com/memex-explorer/memex-explorer
$ cd memex-explorer
$ vagrant up
```

The installation process for the virtual machine can take about an hour, depending on the speed of your Internet connection, as it builds and provisions the Memex Explorer system.  Once it is running, you should receive a message stating that Memex Explorer is running locally on port 8000, which you will then be able to access from your web browser.


# Deploying

The documentation for remote deployment to EC2 is currently a work in progress.  For now, refer to https://github.com/memex-explorer/memex-explorer/issues/559


# Testing
* To run memex-explorer tests, use the command from within an active environment:
```
$ py.test
```

# Modifying Stylesheets
If you need to make changes to the .scss stylesheets, [Compass](http://compass-style.org/) is a useful tool. The following are instructions on how to install compass without using `sudo`.
* For Mac users, add this line to your `~/.bash_profile`:
```
export PATH=/Users/<username>/.gem/ruby/<ruby version>/bin:$PATH
```
Then run `$ gem install compass --user-install`. This will install Compass on your system.
* To make changes to the stylesheets, do:
```
$ cd ../
$ compass watch
```

# Building the Documentation
The project documentation is written in [reStructuredText](http://docutils.sf.net/rst.html) and can be built using the popular [Sphinx](http://sphinx-doc.org/) tool. 

```
$ cd docs
$ make html
```

# Administration

To access the administration panel, navigate to http://localhost:8000/admin (or the equivalent deployed URL) after starting Memex Explorer. Here you will be able to view and make manual changes to the database.

The documentation is then available within `build/html/index.html`
