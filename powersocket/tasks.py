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
        print schedule.TimeSlot.all()
        print 'Checking schedule: ' + schedule.description

        for timeslot in schedule.TimeSlot.all():
            print 'Checking time slot: ' + schedule.start_time + '-' + schedule.end_time + ' (' + ', '.join(day.day for day in self.days_of_week.all()) + ')'
            if now >= timeslot.start_time and now <= timeslot.end_time:
                print ' - Schedule is active!'
                for socket in sockets:
                    print '...Checking light: ' + socket.name


#    logger.info("Start task")
#    now = datetime.now()
#    result = loopcheck.check_state()
#    logger.info('Task finished: result = ' + result)
