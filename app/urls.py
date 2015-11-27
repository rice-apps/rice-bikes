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
    url(r'^(?P<pk>\d+)/buy_back_detail/$', views.BuyBackDetail.as_view(), name='buy_back_detail'),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^rental/$', views.rental, name='rental'),
    url(r'^refurbished/$', views.refurbished, name='refurbished'),
    url(r'^buy_back/$', views.buy_back, name='buy_back'),
    url(r'^new_rental/$', views.new_rental, name='new_rental'),
    url(r'^new_refurbished/$', views.new_refurbished, name='new_refurbished'),
    url(r'^new_buy_back/$', views.new_buy_back, name='new_buy_back'),
    url(r'^balance/$', views.balance, name='balance'),
    url(r'^revenue_update/$', views.revenue_update, name='revenue_update'),

    url(r'^edit_misc_revenue_update/(?P<misc_id>\d+)', views.edit_misc_revenue_update, name='edit_misc_revenue_update'),


    url(r'^bike_inventory/$', views.bike_inventory, name='bike_inventory'),
    url(r'^orders/$', views.orders, name='orders'),

    # sub-urls of detail
    # edit
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/edit/$', views.update,
        {'num_parent_args': 1},
        name='edit_1'),
    url(r'^(?P<bike_pk>\d+)/(?P<parent_url>\w+)/(?P<trans_pk>\d+)/edit/$', views.update,
        {'num_parent_args': 2},
        name='edit_2'),

    # mark_as_completed
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/mark_as_completed/$', views.mark_as_completed,
        {'num_parent_args': 1},
        name='mark_as_completed_1'),
    url(r'^(?P<bike_pk>\d+)/(?P<parent_url>\w+)/(?P<trans_pk>\d+)/mark_as_completed/$', views.mark_as_completed,
        {'num_parent_args': 2},
        name='mark_as_completed_2'),

    # assign_items
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/assign_items/$', views.assign_items,
        {'num_parent_args': 1},
        name='assign_items_1'),
    url(r'^(?P<bike_pk>\d+)/(?P<parent_url>\w+)/(?P<trans_pk>\d+)/assign_items/$', views.assign_items,
        {'num_parent_args': 2},
        name='assign_items_2'),

    # delete_transaction
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/delete_transactions/$', views.delete_transaction,
        name='delete_transaction'),

    # detail paths
    url(r'^(?P<parent_url>\w+)/(?P<trans_pk>\d+)/detail/$', views.detail, {'num_parent_args': 1},
        name='detail_1'),
    url(r'^(?P<bike_pk>\d+)/(?P<parent_url>\w+)/(?P<trans_pk>\d+)/detail/$', views.detail, {'num_parent_args': 2},
        name='detail_2'),

    url(r'^about/$', views.about, name='about'),


    # sold items
    url(r'^sold_items/$', views.sold_items, name='sold_items'),
    url(r'^sold_tasks/$', views.sold_tasks, name='sold_tasks'),
    url(r'^sold_parts/$', views.sold_parts, name='sold_parts'),
    url(r'^sold_accessories/$', views.sold_accessories, name='sold_accessories'),
    url(r'^sold_buy_backs/$', views.sold_buy_backs, name='sold_buy_backs'),

)

urlpatterns += staticfiles_urlpatterns()