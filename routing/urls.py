from django.conf.urls import url
from routing.views import *

urlpatterns = [
    url(r'^simple_route\/$', simple_route),
    url(r'^simple_route\/(?P<data>.*)\/?$', simple_route),
    url(r'^slug_route\/(?P<data>.*)\/?$', slug_route),
    url(r'^sum_route\/(?P<data>.*)\/?$', sum_route),
    url(r'^sum_get_method\/$', sum_get_method),
    url(r'^sum_post_method\/$', sum_post_method)
]
