from django.conf.urls import patterns, url
from fizzbuzz import views

urlpatterns = patterns('',
    url(r'^calculate/([0-9]+)/$', views.calculate, name='calculate'),
)
