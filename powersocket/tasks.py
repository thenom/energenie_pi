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
    sockets = Socket.objects.all()
    schedules = Schedule.objects.all()
    for schedule in schedules:
        now = datetime.now()
        print 'Checking schedule: ' + schedule.description

        for timeslot in schedule.time_slots.all():
            print 'Checking time slot: ' + timeslot.start_time.strftime('%H:%M') + '-' + timeslot.end_time.strftime('%H:%M') + ' (' + ', '.join(day.day for day in timeslot.days_of_week.all()) + ')'
            if now.time() >= timeslot.start_time and now.time() <= timeslot.end_time:
                print ' - Schedule is active!'
                for socket in sockets:
                    print '...Checking light: ' + socket.name


#    logger.info("Start task")
#    now = datetime.now()
#    result = loopcheck.check_state()
#    logger.info('Task finished: result = ' + result)
