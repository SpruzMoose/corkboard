from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
        # example: /
        url(r'^$', views.index, name='index'),
        # example: /login/
        url(r'^login/$', views.login, name='login'),
        # example: /logout/
        url(r'^logout/$', views.logout, name='logout'),
        # example: /home/BarryLyndon
        url(r'^home/(?P<user_name>\w+)/$', views.user, name='home'),
        # example: /pin/12345
        url(r'^pin/(?P<pin_id>\d+)/$', views.pin, name='pin'),
        # example: /board/Just%20Barry%20Things
        url(r'^board/(?P<board_name>[^/]+)/$', views.board, name='board'),
        # example: /pintoboard/12345 (POST)
        url(r'^pintoboard/(?P<pin_id>\d+)/$', views.pintoboard, name='pintoboard'),
        # example: /unpin/12345 (POST)
        url(r'^unpin/(?P<pin_id>\d+)/$', views.unpin, name='unpin'),
)
