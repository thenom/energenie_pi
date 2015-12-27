from django.template import loader
from django.http import HttpResponse

from .models import Socket

# Create your views here.
def index(request):
    sockets = Socket.objects.all()
    template = loader.get_template('powersocket/socketcontrol.html')
    context = {
        'sockets': sockets,
    }
    return HttpResponse(template.render(context, request))
