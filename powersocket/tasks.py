from celery.task.schedules import crontab
from celery.decorators import periodic_task 
#from powersocket.utils import loopcheck
from powersocket.models import Socket, Schedule
from celery.utils.log import get_task_logger
from datetime import datetime


logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def statecheck():
    schedules = Schedule.objects.all()
    sockets_checked = []
    now = datetime.now()

    print '---Starting task (' + str(now.time()) + ')'
    for schedule in schedules:
        sockets_on = False
        print 'Checking schedule: ' + schedule.description

        for timeslot in schedule.time_slots.all():
            print 'Checking time slot: ' + timeslot.start_time.strftime('%H:%M') + '-' + timeslot.end_time.strftime('%H:%M') + ' (' + ', '.join(day.day for day in timeslot.days_of_week.all()) + ')'

            if now.time() >= timeslot.start_time and now.time() <= timeslot.end_time and timeslot.days_of_week.filter(python_dayofweek=now.weekday()).exists():
                print ' - Schedule is active!'
                sockets_on = True
           
        for socket in schedule.socket.all():
            print '...Checking socket: ' + socket.name
            if socket not in sockets_checked:
                sockets_checked.append(socket)

            if socket.current_state != sockets_on and socket.schedule_override == False:
                if sockets_on == True:
                    print '......turning light on'
                else:
                    print '......turning light off'
                socket.current_state = sockets_on
                socket.last_state_change = 's'
                socket.save()
           
    print 'Sockets checked: ' + ', '.join(socket.name for name in sockets_checked)
    print 'Cleaning up sockets...'
    for socket in Socket.objects.all():
        if socket not in sockets_checked:
            print 'Checking socket: ' + socket.name
            if socket.current_state == True and socket.schedule_override == False:
                print '......turning socket off'
                socket.current_state = False
                socket.last_state_change = 's'
                socket.save()

    print '---Task finished'

#    logger.info("Start task")
#    now = datetime.now()
#    result = loopcheck.check_state()
#    logger.info('Task finished: result = ' + result)
