from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app.forms import CustomerForm, RepairsForm, PartCategoryForm

from app import views

urlpatterns = patterns(
    '',
    url(r'^history/$', views.history, name='history'),
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.TransactionWizard.as_view([CustomerForm, RepairsForm, PartCategoryForm]), name="new"),
    url(r'^(?P<pk>\d+)/rental_detail/$', views.RentalDetail.as_view(), name='rental_detail'),
    url(r'^(?P<pk>\d+)/refurbished_detail/$', views.RefurbishedDetail.as_view(), name='refurbished_detail'),
    url(r'^(?P<pk>\d+)/(?P<parent_url>\w+)/edit/$', views.update, name='edit'),
    url(r'^(?P<pk>\d+)/mark_completed/$', views.mark_as_completed, name='mark_completed'),
    url(r'^(?P<pk>\d+)/(?P<parent_url>\w+)/detail/$', views.TransactionDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/(?P<parent_url>\w+)/detail_complete/$', views.TransactionDetailComplete.as_view(),
        name='detail_complete'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^rental/$', views.rental, name='rental'),
    url(r'^refurbished/$', views.refurbished, name='refurbished'),
    url(r'^new_rental/$', views.new_rental, name='new_rental'),
    url(r'^new_refurbished/$', views.new_refurbished, name='new_refurbished'),
    url(r'^balance/$', views.balance, name='balance'),
    url(r'^revenue_update/$', views.revenue_update, name='revenue_update'),
    url(r'^orders/$', views.order, name='orders'),
    url(r'^make_order/$', views.make_order, name='make_order'),
    url(r'^installed_parts', views.used_parts, name='used_parts'),
)

urlpatterns += staticfiles_urlpatterns()