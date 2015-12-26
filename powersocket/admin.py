from django.contrib import admin

# Register your models here.
from .models import Socket, Schedule, DaysOfTheWeek, TimeSlot

admin.site.register(Socket)
admin.site.register(Schedule)
admin.site.register(DaysOfTheWeek)
admin.site.register(TimeSlot)
