from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('app.urls', namespace="app")),
    url(r'^admin/', include(admin.site.urls)),
)
