from celery.task.schedules import crontab, timedelta
from celery.decorators import periodic_task 
#from celery.task import PeriodicTask
#from powersocket.utils import loopcheck
from powersocket.models import Socket, Schedule, DaysOfTheWeek
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta


logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(timedelta(seconds=10)))
def statecheck():
    schedules = Schedule.objects.all()
    sockets_checked = []

    print '---Starting task (' + str(datetime.now()) + ')'
    for schedule in schedules:
        deviated_now = datetime.now() + timedelta(minutes=-schedule.current_random_deviation)
        current_day = DaysOfTheWeek.objects.get(python_dayofweek = deviated_now.weekday())
        change_socket = False
        sockets_on = False
        print 'Checking schedule: ' + schedule.description + ' (minute deviation: ' + str(schedule.current_random_deviation) + ')'

        for timeslot in schedule.time_slots.all():
            print 'Checking time slot: ' + str(timeslot)

            if str(deviated_now.weekday()) in timeslot.days_of_week:
                if deviated_now.time().strftime('%H:%M') == timeslot.start_time.strftime('%H:%M'):
                    print ' - Triggering socket switch on! (time deveation: ' + str(schedule.current_random_deviation) + ')'
                    sockets_on = True
                    change_socket = True
                    timeslot.save()    # trigger non manual time generation
                elif deviated_now.time().strftime('%H:%M') == timeslot.end_time.strftime('%H:%M'):
                    print ' - Triggering socket switch off! (time deveation: ' + str(schedule.current_random_deviation) + ')'
                    change_socket = True
                    timeslot.save()    # trigger non manual time generation

            
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
                    schedule.save()     # trigger save to generate new random deviation value
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
