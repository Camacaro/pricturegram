"""platzigram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

# Modulo de URLs

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from platzigram import views as local_views
from posts import views as posts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello-world/', local_views.hello_world),
    path('timers/', local_views.timers),
    path('sorted/', local_views.sort_integers),
    path('hi/<str:name>/<int:age>/', local_views.say_hi),

    path('posts-test/', posts_views.list_posts_test),
    path('posts/', posts_views.list_posts),

    # servir archivos staticos, imagenes
    # https://docs.djangoproject.com/en/3.1/ref/settings/
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
