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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from platzigram import views as local_views
from posts import views as posts_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello-world/', local_views.hello_world, name='hello-world'),
    path('timers/', local_views.timers, name='timers'),
    path('sorted/', local_views.sort_integers, name='sorted'),
    path('hi/<str:name>/<int:age>/', local_views.say_hi, name='hi'),



    path('posts-test/', posts_views.list_posts_test),
    # Esto es para incluir las dos rutas de abajo en una en otro archivo
    path('', include( ('posts.urls', 'posts'), namespace='posts') ),
    # el / es innecesario por eso se deja en vacio
    # path('', posts_views.list_posts, name='feed'),
    # path('posts/new', posts_views.create_post, name='create_post'),

    # argumentos
    # 'users/' : init path
    # 'users.urls' : file where are the urls
    # 'users' : aplication -> la aplicacion
    # namespace : namespace de las urls 
    path('users/', include( ('users.urls', 'users'), namespace='users' ) ),
    # path('users/login/', users_views.login_view, name='login'),
    # path('users/logout/', users_views.logout_view, name='logout'),
    # path('users/signup/', users_views.signup_view, name='signup'),
    # path('users/me/profile', users_views.update_profile, name='update_profile'),


    # servir archivos staticos, imagenes
    # https://docs.djangoproject.com/en/3.1/ref/settings/
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
