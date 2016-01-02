from celery.task.schedules import crontab, timedelta
from celery.decorators import periodic_task 
#from celery.task import PeriodicTask
#from powersocket.utils import loopcheck
from powersocket.models import Socket, Schedule, DaysOfTheWeek
from celery.utils.log import get_task_logger
from datetime import datetime


logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(timedelta(seconds=30)))
def statecheck():
    schedules = Schedule.objects.all()
    sockets_checked = []
    now = datetime.now()
    current_day = DaysOfTheWeek.objects.get(python_dayofweek = now.weekday())

    print '---Starting task (' + str(now.time()) + ')'
    for schedule in schedules:
        change_socket = False
        sockets_on = False
        print 'Checking schedule: ' + schedule.description

        for timeslot in schedule.time_slots.all():
            print 'Checking time slot: ' + timeslot.start_time.strftime('%H:%M') + '-' + timeslot.end_time.strftime('%H:%M') + ' (' + ', '.join(day.day for day in timeslot.days_of_week.all()) + ')'

            if timeslot.days_of_week.filter(python_dayofweek=now.weekday()).exists():
                if now.time().strftime('%H:%M') == timeslot.start_time.strftime('%H:%M'):
                    print ' - Schedule is active!'
                    sockets_on = True
                    change_socket = True
                elif now.time().strftime('%H:%M') == timeslot.end_time.strftime('%H:%M'):
                    change_socket = True

            
        # actually do the socket changes
        if change_socket == True:
            for socket in schedule.socket.all():
                print '...Checking socket: ' + socket.name
                if socket not in sockets_checked:
                    sockets_checked.append(socket)
 
                if socket.current_state != sockets_on:
                    if sockets_on == True:
                        print '......turning socket on'
                    else:
                        print '......turning socket off'
                    socket.current_state = sockets_on
                    socket.save()
           
    print '---Task finished'


# A periodic task that will run every minute (the symbol "*" means every)
#@periodic_task(run_every=(crontab(hour="0", minute="1", day_of_week="*")))
#def cleanup():
#    now = datetime.now()
#    current_day = DaysOfTheWeek.filter(python_dayofweek = now.dayofweek())
#
#    for day in DaysOfTheWeek:
#        if day != current_day:
#            for timeslot in 
