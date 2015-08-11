from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app import views

urlpatterns = patterns(
    '',
    url(r'^history/$', views.history, name='history'),
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.create_transaction, name="new"),
    url(r'^(?P<pk>\d+)/rental_detail/$', views.RentalDetail.as_view(), name='rental_detail'),
    url(r'^(?P<pk>\d+)/refurbished_detail/$', views.RefurbishedDetail.as_view(), name='refurbished_detail'),

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

    # sub-urls of detail
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/edit/$', views.update, name='edit_1'),
    url(r'^(?P<parent_url>\w+)/(?P<bike_pk>\d+)/(?P<trans_pk>\d+)/edit/$', views.update, name='edit_2'),

    """
    EDIT THESE MOTHER MOTHERS TO THE RIGHT REGEX/VIEW/NAME
    # sub-urls of detail
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/edit/$', views.update, name='edit_1'),
    url(r'^(?P<parent_url>\w+)/(?P<bike_pk>\d+)/(?P<trans_pk>\d+)/edit/$', views.update, name='edit_2'),

        # sub-urls of detail
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/edit/$', views.update, name='edit_1'),
    url(r'^(?P<parent_url>\w+)/(?P<bike_pk>\d+)/(?P<trans_pk>\d+)/edit/$', views.update, name='edit_2'),

        # sub-urls of detail
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/edit/$', views.update, name='edit_1'),
    url(r'^(?P<parent_url>\w+)/(?P<bike_pk>\d+)/(?P<trans_pk>\d+)/edit/$', views.update, name='edit_2'),

    """

    # detail paths
    url(r'^(?P<parent_url>\w+)/(?P<pk>\d+)/detail/$', views.detail,
        name='detail_1'),
    url(r'^rental_detail/(?P<rental_pk>\d+)/(?P<trans_pk>\d+)/detail/$', views.detail,
        {'parent_url': 'rental_detail'},
        name='rental_detail_trans_detail'),


)

urlpatterns += staticfiles_urlpatterns()