from django.conf.urls import patterns, url
from siteusers import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^update$', views.update, name='update'),
    url(r'^view$', views.view, name='view'),
    url(r'^all$', views.all, name='all'),
    url(r'^authenticate$', views.authenticate, name='authenticate'),
    url(r'^add$', views.add, name='add')
)
