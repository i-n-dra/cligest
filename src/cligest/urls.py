"""
URL configuration for foobar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles import views as staticfiles
from django.urls import path, re_path, include
from gestion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # default views
    path("admin/", admin.site.urls),
    re_path(r"^static/(?P<path>.*)$", staticfiles.serve),

    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('management/', include('gestion.urls')),
    path('login/', include('login.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)