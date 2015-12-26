from django.db import models

# Create your models here.
class DaysOfTheWeek(models.Model):
    day = models.CharField(max_length=20)
    python_dayofweek = models.IntegerField(default=0)

    def __str__(self):
        return self.day

class Socket(models.Model):
    LAST_STATE_CHANGE = (
        ('m', 'Manual'),
        ('s', 'Schedule'),
    )

    socket_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    current_state = models.BooleanField(default=0)
    last_state_change = models.CharField(choices=LAST_STATE_CHANGE,default='m', max_length=1)

    def __str__(self):
        return self.name
 
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.ManyToManyField(DaysOfTheWeek)

    def __str__(self):
        return self.start_time.strftime('%H:%M') + '-' + self.end_time.strftime('%H:%M') + ' (' + ', '.join(day.day for day in self.days_of_week.all()) + ')'

class Schedule(models.Model):
    description = models.CharField(max_length=200,default='')
    socket = models.ManyToManyField(Socket)
    time_slots = models.ManyToManyField(TimeSlot)
    overridden = models.BooleanField(default=False)

    def __str__(self):
        return self.description
