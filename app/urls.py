from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app.forms import CustomerForm, RepairsForm

from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<customer_id>\d+)/mark_completed/$', views.mark_as_completed, name='mark_completed'),
    url(r'^(?P<pk>\d+)/edit/$', views.CustomerUpdate.as_view(), name='edit'),
    url(r'^create_order/$', views.CustomerWizard.as_view([CustomerForm, RepairsForm]), name='create_order'),
    url(r'^(?P<pk>\d+)/$', views.CustomerDetail.as_view(), name='detail'),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name="logout"),
)

urlpatterns += staticfiles_urlpatterns()