from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update_socket/([0-9]+)/$', views.update_socket, name='update_socket'),
]
