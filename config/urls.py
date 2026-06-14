"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from config import settings
from src.adminpanel.api import api

from django.contrib.sitemaps.views import sitemap

from .views import page_not_found_view, server_not_work

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('select2/', include('django_select2.urls')),

    path('adminpanel/', include('src.adminpanel.urls')),

    path('', include('src.frontend.urls'))

    #path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found_view
handler500 = server_not_work