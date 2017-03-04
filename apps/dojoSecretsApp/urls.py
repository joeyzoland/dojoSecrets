from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^validator$', views.validator),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^make_secret$', views.make_secret),
    url(r'^order_secret$', views.order_secret),
    url(r'^like$', views.like),
    url(r'^update$', views.update),
    url(r'^delete$', views.delete),
    url(r'^logout$', views.logout),
]
