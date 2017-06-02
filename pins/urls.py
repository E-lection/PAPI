from django.conf.urls import url

from . import views

app_name = 'pins'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_pin_code/station_id/(?P<station_id>[0-9]+)/voter_id/(?P<voter_id>[0-9]+)/$', views.get_pin_code, name='get_pin_code')
]
