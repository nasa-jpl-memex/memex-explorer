#!/bin/bash

NAME="memex_explorer"                                  # Name of the application
DJANGODIR=/vagrant/source             # Django project directory
SOCKFILE=/home/vagrant/gunicorn.sock # we will communicte using this unix socket
USER=vagrant
GROUP=vagrant
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=memex.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=memex.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

echo $DJANGODIR
echo gunicorn ${DJANGO_WSGI_MODULE}:application
echo `pwd`
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER --group $GROUP \
  --bind unix:$SOCKFILE \
#  --log-level=debug \
#  --log-file=-
