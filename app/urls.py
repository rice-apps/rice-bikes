from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app.forms import CustomerForm, RepairsForm

from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.TransactionWizard.as_view([CustomerForm, RepairsForm]), name="new"),
    url(r'^(?P<pk>\d+)/$', views.TransactionDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.TransactionUpdate.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/mark_completed/$', views.mark_as_completed, name='mark_completed'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
)

urlpatterns += staticfiles_urlpatterns()