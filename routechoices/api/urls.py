from django.conf.urls import url

from routechoices.api import views

urlpatterns = [
    url(r'^$', views.api_root, name='api_root'),
    url(r'^device_id/?$', views.get_device_id, name='device_id_api'),
    url(r'^imei/?$', views.get_device_for_imei, name='device_imei_api'),
    url(
        r'^gps_seuranta_proxy/?$',
        views.gps_seuranta_proxy,
        name='gps_seuranta_proxy'
    ),
    url(r'^pwa/?$', views.pwa_api_gw, name='pwa_api_gw'),
    url(r'^time/?$', views.get_time, name='time_api'),
    url(r'^user/search/?$', views.user_search, name='user_search_api'),
    url(r'^device/search/?$', views.device_search, name='device_search_api'),
    url(r'^traccar/?$', views.traccar_api_gw, name='traccar_api_gw'),
    url(r'^garmin/?$', views.garmin_api_gw, name='garmin_api_gw'),
    url(
        r'^events/?$',
        views.event_list,
        name='event_list'
    ),
    url(
        r'^events/(?P<aid>[0-9a-zA-Z_-]+)/?$',
        views.event_detail,
        name='event_detail'
    ),
    url(
        r'^events/(?P<aid>[0-9a-zA-Z_-]+)/map/?$',
        views.event_map_download,
        name='event_map_download'
    ),
    url(
        r'^events/(?P<aid>[0-9a-zA-Z_-]+)/extra_map/(?P<index>\d+)?$',
        views.event_extra_map_download,
        name='event_extra_map_download'
    ),
    url(
        r'^events/(?P<aid>[0-9a-zA-Z_-]+)/data/?$',
        views.event_data,
        name='event_data'
    ),
    url(
        r'^events/(?P<aid>[0-9a-zA-Z_-]+)/map_details/?$',
        views.event_map_details,
        name='event_map_details'
    ),
    url(
        r'^events/(?P<aid>[0-9a-zA-Z_-]+)/notice/?$',
        views.event_notice,
        name='event_notice'
    ),
    url(
        r'^competitor/(?P<aid>[0-9a-zA-Z_-]+)/gpx$',
        views.competitor_gpx_download,
        name='competitor_gpx_download'
    ),
]
