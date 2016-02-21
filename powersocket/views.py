from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .models import Socket, Schedule

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
