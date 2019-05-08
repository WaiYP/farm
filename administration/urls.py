from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
app_name = "administration"
urlpatterns =[
    url(r'^$', views.index, name='index'),
    url(r'^user_login/', views.user_login, name='user_login'),
    # url(r'^admin_home/$', views.home, name='home'),
    # url(r'^$', auth_views.login, {'template_name': 'administration/login.html'}, name='login'),
    # url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # url(r'^change_password/$', views.change_password, name='change_password'),
    # url(r'^city/$', views.city, name='city'),
    # url(r'^city/add/$', views.add_city, name='add_city'),
    # url(r'register/$', views.register, name='user_register'),
    # url(r'^profile/$', views.view_profile, name='view_profile'),
    # url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    # url(r'^users/$', views.users, name='users'),
    # url(r'^routes/add/$', views.add_route, name='add_route'),
    # url(r'^routes/edit/(?P<id>\d+)/$', views.edit_route, name='edit_route'),
    # url(r'^routes/$', views.routes, name='routes'),
    # url(r'^stop_points/(?P<id>\d+)/$', views.stop_points, name='stop_points'),
    # url(r'^bus/add/$', views.bus_registration, name='add_bus'),
    # url(r'^bus/edit/(?P<id>\d+)/$', views.bus_edit, name='bus_edit'),
    # url(r'^bus/add_seat/(?P<id>\d+)/$', views.add_seats, name='add_seats'),
    # url(r'^bus/$', views.bus_list, name='bus_list'),
    # url(r'^schedule/add/$', views.add_schedule, name='add_schedule'),
    # url(r'^schedule/edit/(?P<id>\d+)/$', views.edit_schedule, name='schedule_edit'),
    # url(r'^schedule/detail/(?P<sid>\d+)/(?P<rid>\d+)/$', views.schedule_detail_popup, name='schedule_detail'),
    # url(r'^schedule/$', views.schedule_list, name='schedule_list'),
    # url(r'^extra_service/$', views.extra_service, name='extra_service'),
    # url(r'^extra_service/add$', views.add_extra_service, name='add_extra_service'),
    # url(r'^ferry_service/$', views.ferry_locations, name='ferry_service'),
    # url(r'^ferry_service/add$', views.add_ferry_location, name='add_ferry_service'),
    # url(r'^role/$', views.role, name='role'),
    # url(r'^role/add$', views.add_role, name='add_role'),
    # url(r'^driver/$', views.driver, name='driver'),
    # url(r'^drivers/add$', views.add_driver, name='add_driver'),
]