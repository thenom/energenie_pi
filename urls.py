from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update_socket/([A-Za-z0-9\s]+)/$', views.update_socket, name='update_socket'),
    url(r'^sched_check$', views.sched_check, name='sched_check'),
]
