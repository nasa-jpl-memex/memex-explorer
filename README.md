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

The current method for deploying to the web is to deploy to ec2 by running a
fabric script with a few environment variables set.

$ git clone https://github.com/memex-explorer/memex-explorer
$ cd memex-explorer/deploy
$ conda env create --file deploy_environment.yml
$ source activate memex_deploy
$ cp deploy_ec2.sh nocommit.sh

Now edit the file nocommit.sh. It will contain three environment variables
which you must set and which you must not commit to the public repository.

    AWS_KEY_ID: The key id for your aws account

    AWS SECRET: The key secret for your aws account

    HTPASSWD_PATH: The HTTP login password path. This file should have been
    given to you.  Place it at a location not tracked by git and enter the absolute
    path to this location in the value of this variable.

Additionally, you can choose to deploy a different git branch than the production branch.

Once you have set these variables, you can start a new instance with `source nocommit.sh`, which
will create an ec2 instance, place a login key for it in memex-explorer/deploy/keys and run the deploy script on the new instance.

The login key for the new instance will be given three names:

    One based on the IP address of the new server.

    One based on the creation time of the new server.

    latest.pem, a convenience to logging in to the most-recently-created server.

To connect to a instance given an IP address of 54.167.11.71, log in with the command

    ssh -i keys/ec2-54.167.11.71.pem vagrant@54.167.11.71

After the setup script is done running, you will be able to access the application by entering the IP address into your browser.

# Testing

To run memex-explorer tests, use the following command from within an active environment:
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

The documentation is then available within `build/html/index.html`

# Administration

To access the administration panel, navigate to http://localhost:8000/admin (or the equivalent deployed URL) after starting Memex Explorer. Here you will be able to view and make manual changes to the database.
