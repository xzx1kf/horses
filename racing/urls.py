from django.conf.urls import patterns, url

from racing import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^layem/$', views.layem, name='layem'),
                       url(r'^(?P<meeting_id>\d+)/$', views.meeting_detail, name='meeting_detail'),
                       url(r'^update/$', views.update, name='update'),
)
