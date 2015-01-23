from django.conf.urls import patterns, url

from racing import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
)
