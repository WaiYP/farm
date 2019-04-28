from django.conf.urls import url
from . import views

app_name = "dashboard"
urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^about/$',views.about,name='about'),
    url(r'^product/$',views.product,name='product'),
    url (r'^news/$',views.news,name='news'),
    url (r'^newdetail/$',views.newdetail,name='newdetail'),
    url (r'^shop/$',views.shop,name='shop'),
    url (r'^farmingpractice/$',views.farmingpractice,name='farmingpractice'),
    url(r'^contact/$', views.contact, name='contact'),

]