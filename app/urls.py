from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'(?P<pk>\d+)/', views.CustomerUpdate.as_view(), name='detail'),
)