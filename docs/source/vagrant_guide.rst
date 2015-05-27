#############################################
Developing with Vagrant
#############################################

Memex Explorer is currently developed and deployed with Vagrant and
Salt.  Vagrant is a software tool that simplifies the process of
developing on virtual machines in a way that is reproducible across
multiple development environments.  The "heavy lifting" is done by
Salt, a flexible configuration management system that is run by the
Vagrant provisioning tool.

This is a short guide explaining how to use Vagrant to install and
develop Memex Explorer.

+++++++++
Cheat sheet:
+++++++++

``vagrant up`` - This command attemps to start the virtual machine.
It should always be run in the root directory of memex-explorer.  It
is responsible for mapping the local file system to the virtual
machine and forwarding ports so that the virtual machine "feels" like
the local development environment.  The first time it's run, it will
also call ``vagrant provision``. 

``vagrant provision`` - This command will run the Salt provisioner on
the virtual machine.  This will try to put the virtual machine in a
production-ready state and start up all necessary services.  After the
Salt provisioner is completed, the Memex Explorer process is started
and the user is pointed to localhost:8000.  The process does not end
until it has been terminated.  It is safest to kill a running
``vagrant provision`` using ``vagrant ssh`` and then running
``sudo killall python``.

``vagrant ssh`` - Use this command to log into the virtual box.  You
will have passwordless sudo privileges.

``vagrant reload`` - Use this command to reload the virtual box after
making changes to the Vagrantfile.  This is not needed if you are only
changing the Salt provisioner or the Memex Explorer source code.

``vagrant destroy`` - Use this as a last resort if your virtual box
seems to be corrupted or no longer working.
