from django.db import models
from socket_functions import socket_control

energenie = socket_control()

# Create your models here.
class DaysOfTheWeek(models.Model):
    day = models.CharField(max_length=20,unique=True)
    python_dayofweek = models.IntegerField(default=0)

    def __str__(self):
        return self.day

class Socket(models.Model):
    LAST_STATE_CHANGE = (
        ('m', 'Manual'),
        ('s', 'Schedule'),
    )

    socket_id = models.IntegerField(default=0,unique=True)
    name = models.CharField(max_length=200)
    current_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Socket, self).save(*args, **kwargs) # Call the "real" save() method.
        print 'Physically setting the socket (' + self.name + ') switch to ' + str(self.current_state)
        if self.current_state == True:
             energenie.socket_on(self.id)
        else:
             energenie.socket_off(self.id)
 
class TimeSlot(models.Model):
    start_time = models.TimeField(help_text='Seconds are ignored')
    end_time = models.TimeField(help_text='Seconds are ignored')
    days_of_week = models.ManyToManyField(DaysOfTheWeek)

    def __str__(self):
        return self.start_time.strftime('%H:%M') + '-' + self.end_time.strftime('%H:%M') + ' (' + ', '.join(day.day for day in self.days_of_week.all()) + ')'

class Schedule(models.Model):
    description = models.CharField(max_length=200,default='')
    socket = models.ManyToManyField(Socket)
    time_slots = models.ManyToManyField(TimeSlot, blank=True)

    def __str__(self):
        return self.description
