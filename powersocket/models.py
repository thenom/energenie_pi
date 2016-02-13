from django.db import models
from socket_functions import socket_control
import random
from datetime import timedelta
from django.utils import timezone
from astral import Astral

energenie = socket_control()

# Create your models here.
class AstralCities(models.Model):
    city = models.CharField(max_length=40,unique=True)

    def __str__(self):
        return self.city
    class Meta:
        verbose_name_plural = "AstralCities"

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
    TIME_MODE = (
        ('M','Manually set'),
        ('dawn', 'Dawn'),
        ('sunrise','Sunrise'),
        ('sunset','Sunset'),
        ('noon','Noon'),
        ('dusk','Dusk'),
    )

    city = models.ForeignKey(AstralCities, default=1)
    start_time_mode = models.CharField(max_length=10, choices=TIME_MODE, default='M')
    start_time = models.TimeField(help_text='Seconds are ignored and time will be overwritten if manual mode is not selected')
    end_time_mode = models.CharField(max_length=10, choices=TIME_MODE, default='M')
    end_time = models.TimeField(help_text='Seconds are ignored and time will be overwritten if manual mode is not selected')
    days_of_week = models.ManyToManyField(DaysOfTheWeek)

    def __str__(self):
        return self.start_time.strftime('%H:%M') + '(' + self.start_time_mode + ')-' + self.end_time.strftime('%H:%M') + '(' + self.end_time_mode + ') (' + ', '.join(day.day for day in self.days_of_week.all()) + ')'

    def save(self, *args, **kwargs):
        if self.start_time_mode != 'M':
            self.start_time = self.get_time(self.start_time_mode, self.city)
        if self.end_time_mode != 'M':
            self.end_time = self.get_time(self.end_time_mode, self.city)
        super(TimeSlot, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_time(self, mode, city):
        a = Astral()
        now = timezone.now()
        cur_city = a[city]
        sun = cur_city.sun(date=timezone.now(), local=True)
        if sun[mode] < now:
            sun = cur_city.sun(date=timezone.now() + timedelta(days=1), local=True)
        print 'Generated ' + mode + ' time: ' + str(sun[mode]) + ' (using current time ' + str(now) + ')'
        
        return sun[mode].time()
        


class Schedule(models.Model):
    description = models.CharField(max_length=200,default='')
    socket = models.ManyToManyField(Socket)
    time_slots = models.ManyToManyField(TimeSlot, blank=True)
    random_range = models.IntegerField(help_text='Random minutes range to apply before\\after the actual start time')
    current_random_deviation = models.IntegerField(default=0)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        rand_num = random.randint(0,self.random_range*2)
        rand_num = rand_num - self.random_range
        self.current_random_deviation = rand_num
        super(Schedule, self).save(*args, **kwargs) # Call the "real" save() method.
