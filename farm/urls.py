"""farm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import include, url
from django.template.context_processors import static
from django.views.generic import TemplateView

from dashboard import views
from farm import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/',include('dashboard.urls')),
    url(r'^administration/',include('administration.urls')),
    url(r'^contact/', TemplateView.as_view(template_name='../templates/contact.html'),name='contact'), # /admin,/contact,/booking
]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)