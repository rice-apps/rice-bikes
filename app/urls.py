from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/edit$', views.CustomerUpdate.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/$', views.CustomerDetail.as_view(), name='detail'),
)

urlpatterns += staticfiles_urlpatterns()