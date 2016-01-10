# Energenie Pi Control

This is a Django project that uses Celery for scheduling and provides a basic control webpage.  It is designed for use with the Raspberry Pi and the Energenie Pi Hat (ENER314\ENER314).  The default is to use a local SQLLite DB file but this can be changed (https://docs.djangoproject.com/en/1.9/ref/settings/#databases). It also requires a RabbitMQ setup for Celery transactions.

Basic useful feature list:

 * Setup and modify sockets for control
 * Setup multiple schedules and control multiple sockets via each schedule
 * Add multiple time slots to each schedule
 * Basic web page for control and sockets current status

Dependencies:

 * Django 1.8
 * RabbitMQ server
 * Raspberry Pi with Networking
 * Energenie Raspberry Pi Hat (ENER314\ENER314)   # See Note1
 * Energenie python module # See Note2


I have created a startup script for this as there are 3 processes required for this to fully function but it is basic and doesn't control the django server properly as it spawns other subprocesses and the main process ends:
```
./run.sh
```
If you want to manually run the 3 services then run these from the energenie directory:

Celerybeat - Creates the scheduled task at 30 second intervals
```
$ python manage.py celerybeat
```
CeleryD - Processes the task list created by celerybeat
```
$ python manage.py celeryd
```
Django server - This provides the main django framwork admin page and the basic web management page
```
$ python manage.py runserver 0.0.0.0:8000
```

Notes:

1. A Rapberry Pi or the Energenie Hat is not required as the code catches this and disables the control for testing purposes.
2. To install this module just run 'pip install energenie'