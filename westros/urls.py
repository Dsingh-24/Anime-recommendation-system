from django.conf.urls import include, url
from westros.feeds import LatestAnimeFeed

from . import views

app_name = 'westros'

urlpatterns = [
    url(r'^$', views.homepage,name='home'),
    url(r'^home', views.westros,name='index'),
    url(r'^about_us', views.about_us,name='about_us'),
    url(r'^(?P<anime_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<anime_id>[0-9]+)/(?P<l_id>[0-9])/$',views.like,name='like'),
    url(r'^explore',views.explore,name='explore'),
    url(r'^favanime', views.favanime,name='favanime'),
    url(r'^term-&-conditions', views.tc,name='terms'),
    url(r'^login_user', views.login_user,name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^register/$',views.register,name='register'),
    url(r'^search/$',views.search,name='search'),
    url(r'^recommendations/$',views.recommendations,name='recommendations'),    
    url(r'^latestanime',LatestAnimeFeed(),name="latestanime"),
]