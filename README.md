# Energenie Pi Control

This is a Django project that uses Celery for scheduling and provides a basic control webpage.  It is designed for use with the Raspberry Pi and the Energenie Pi Hat (ENER314\ENER314-RT).  The default is to use a local SQLLite DB file but this can be changed (https://docs.djangoproject.com/en/1.9/ref/settings/#databases). It also requires a RabbitMQ\Redis setup for Celery transactions but i have tested with Redis and this also works fine (you just need to install pip module and change BROKER_URL in settings.py).

It check the schedules every second and modifies the state of the socket accordingly.  You can apply a random deviation the the schedule to mimic variations in turning the sockets on and off.  For example, if a schedule is set to turn a light on at 16:30:00 and has a random second value of 30 seconds then the light will turn on between 16:29:30 and 16:30:30.

Basic useful feature list:

 * Setup and modify sockets for control
 * Setup multiple schedules and control multiple sockets via each schedule
 * Add multiple time slots to each schedule
 * Basic web page for control and sockets current status
 * Randomly changes the on\off time based on a deviation value in seconds

# Dependencies

 * Django 1.8
 * RabbitMQ/Redis
 * Raspberry Pi with Networking
 * Energenie Raspberry Pi Hat (ENER314\ENER314-RT)   # See Note1
 
```
yum install MySQL-python
yum install python-devel
pip install django-celery==3.1.17
pip install celery==3.1.19
pip install django==1.8.7
pip install redis   (if using redis backend, see Note2)
```

# Screenshot

![Alt text](/screenshot.png?raw=true "Control page")



# Running

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

To access the control page:
\<host\>:8000/powersocket

To access the admin pages:
\<host\>:8000/admin

# Setup
You will need to modify the run script to match your own working directory.  To get this to work on boot in my setup i just placed this script in rc.local, adding the & at the end to force it to run in the background.  You will also need to modify the celery ampq URL and your MySQL database details in energenie_pi/settings.py to match your own RabbitMQ\Redis\MySQL server setup.  It is currently using a vhost of 'energenie_pi', a user of 'energenie_pi' and password 'Passw0rd'.

You will also need to change your 'ALLOWED_HOSTS' in energenie_pi/settings.py to the URL you are calling for your local setup.

# Notes:

1. A Rapberry Pi or the Energenie Hat is not required as the code catches this and disables the control for testing purposes.
2. If using Redis backend (more lightweight) the BROKER_URL in energenie_pi/settings.py should be similar to: BROKER_URL = 'redis://<host>:6379/0'