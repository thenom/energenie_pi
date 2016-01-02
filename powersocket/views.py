from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .models import Socket

# Create your views here.
def index(request):
    sockets = Socket.objects.all()
    template = loader.get_template('powersocket/socketcontrol.html')
    context = {
        'sockets': sockets,
    }
    return HttpResponse(template.render(context, request))

def update_socket(request, socket_id):
    p = get_object_or_404(Socket, pk=socket_id)

    if request.method == 'POST':
        print request.POST
        print 'Setting state to: ' + request.POST['change_to']
        if request.POST['change_to'] == 'on':
            p.current_state = True
            p.save()
        else:
            p.current_state = False
            p.save()
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('powersocket:index', args=(p.id,)))
        return HttpResponseRedirect(reverse('powersocket:index'))
