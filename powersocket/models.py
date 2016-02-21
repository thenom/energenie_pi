from django.db import models
from socket_functions import socket_control
import random
from datetime import timedelta, datetime
from django.utils import timezone
from astral import Astral
from multiselectfield import MultiSelectField

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

    PYTHON_DAYS = (
        ('0','Monday'),
        ('1','Tuesday'),
        ('2','Wednesday'),
        ('3','Thursday'),
        ('4','Friday'),
        ('5','Saturday'),
        ('6','Sunday'),
    )

    city = models.ForeignKey(AstralCities, default=1)
    start_time_mode = models.CharField(max_length=10, choices=TIME_MODE, default='M')
    start_time = models.TimeField(help_text='Seconds are ignored and time will be overwritten if manual mode is not selected', default='00:00:00')
    end_time_mode = models.CharField(max_length=10, choices=TIME_MODE, default='M')
    end_time = models.TimeField(help_text='Seconds are ignored and time will be overwritten if manual mode is not selected', default='00:00:00')
    days_of_week = MultiSelectField(choices=PYTHON_DAYS)

    def __str__(self):
#        return self.start_time.strftime('%H:%M') + '(' + self.start_time_mode + ')-' + self.end_time.strftime('%H:%M') + '(' + self.end_time_mode + ') (' + ', '.join(day.day for day in self.days_of_week.all()) + ')'
        days_list = []
        for int,day in self.PYTHON_DAYS:
            if int in self.days_of_week:
                days_list.append(day)
        return self.start_time.strftime('%H:%M') + '(' + self.start_time_mode + ')-' + self.end_time.strftime('%H:%M') + '(' + self.end_time_mode + ') (' + ', '.join(days_list) + ')'

    def save(self, *args, **kwargs):
        if self.start_time_mode != 'M':
            self.start_time = self.set_time(self. start_time_mode, self.city, self.days_of_week)
        if self.end_time_mode != 'M':
            self.end_time = self.set_time(self.end_time_mode, self.city, self.days_of_week)
        super(TimeSlot, self).save(*args, **kwargs) # Call the "real" save() method.

    def set_time(self, mode, city, days_of_week):
        now = timezone.now()
        deltadays = 0
        week_day_count = now.weekday()
        a = Astral()
        cur_city = a[city]
        for day_shift in range(1,7):
            if week_day_count > 6:
                week_day_count = 0
            if str(week_day_count) in days_of_week:
                sun = cur_city.sun(date=timezone.now() + timedelta(days=deltadays), local=True)
                if sun[mode] > now:
                    break
            deltadays += 1
            week_day_count +=1
        print 'Generated ' + mode + ' time: ' + str(sun[mode]) + ' using time current time of ' + str(timezone.now()) + ' (' + str(deltadays) + ' days ahead)'

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
