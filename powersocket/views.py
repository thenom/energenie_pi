from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render

from .models import Socket, Schedule, DaysOfTheWeek
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    sockets = Socket.objects.all()
    schedules = Schedule.objects.all()
    template = loader.get_template('powersocket/socketcontrol.html')
    context = {
        'sockets': sockets,
        'schedules': schedules,
    }
    return HttpResponse(template.render(context, request))

def update_socket(request, socket_id):
    if socket_id == 'alloff' or socket_id == 'allon':
        print 'Setting sockets to: ' + socket_id
        for socket in Socket.objects.all():
            socket.override_time_end = datetime.now()
            if socket_id == 'alloff':
                state = False
            elif socket_id == 'allon':
                state = True
            print 'Setting ' + socket.name + ' to: ' + str(state)
            socket.current_state = state
            socket.save()
    else:
        socket = get_object_or_404(Socket, socket_id=socket_id)

        print 'Setting socket ' + socket.name + ' to: ' + request.POST['change_to']
        socket.override_time_end = datetime.now() + timedelta(minutes=10)
        if request.POST['change_to'] == 'on':
            socket.current_state = True
            socket.save()
        else:
            socket.current_state = False
            socket.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    #return HttpResponseRedirect(reverse('powersocket:index', args=(p.id,)))
    return HttpResponseRedirect(reverse('powersocket:index'))

def sched_check(request):
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
                currenttime = datetime.now()
                print '...Checking socket: ' + socket.name
                if socket not in sockets_checked:
                    sockets_checked.append(socket)

                # clear up old override times
                if socket.override_time_end != None:
                    if socket.override_time_end.strftime('%H:$M') < datetime.now().strftime('%H:%M'):
                        socket.override_time_end == None
                        socket.save()

                if socket.current_state != sockets_on:
                    override = False
                    if socket.override_time_end != None:
                        if currenttime.strftime('%H:%M') < socket.override_time_end.strftime('%H:%M'):
                            override = True
                    if override == False:
                        if sockets_on == True:
                            print '......turning socket on'
                        else:
                            print '......turning socket off'
                        schedule.save()     # trigger save to generate new random deviation value
                        socket.current_state = sockets_on
                        socket.override_time_end = None
                        socket.save()
                    else:
                        print 'Scheduled change has been overridden by manual socket state change!  Socket state will not change'

    # clear up old override times
    for socket in Socket.objects.all():
        if socket.override_time_end != None:
            if socket.override_time_end.strftime('%H:%M') < datetime.now().strftime('%H:%M'):
                print 'Clearing overide time for socket: ' + socket.name
                socket.override_time_end = None
                socket.save()

    print '---Task finished'
    return HttpResponse('Scheduled check complete')
