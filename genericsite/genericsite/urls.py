from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'genericsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^siteusers/', include('siteusers.urls')),
    url(r'^fizzbuzz/', include('fizzbuzz.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('siteusers.urls')),
)
