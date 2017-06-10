from django.conf.urls import url

from . import views

ID_REGEX = '[0-9]+'
NAME_REGEX = '[A-z ,.\'-]+'
PIN_CODE_REGEX = '[0-9]{6}'

app_name = 'pins'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_pin_code/station_id/(?P<station_id>' + ID_REGEX +
        ')/voter_id/(?P<voter_id>' + ID_REGEX + ')/$', views.get_pin_code, name='get_pin_code'),
    url(r'^verify_pin_code_and_check_eligibility/station_id/(?P<station_id>' + ID_REGEX + ')/pin_code/(?P<pin_code>' +
        PIN_CODE_REGEX + ')/$', views.verify_pin_code_and_check_eligibility, name='verify_pin_code_and_check_eligibility'),
    url(r'^verify_pin_code_and_make_ineligible/station_id/(?P<station_id>' + ID_REGEX + ')/pin_code/(?P<pin_code>' +
        PIN_CODE_REGEX + ')/$', views.verify_pin_code_and_make_ineligible, name='verify_pin_code_and_make_ineligible')
]
