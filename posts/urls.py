
from django.urls import path

from posts import views

urlpatterns = [
  path(
    route='', 
    # view= views.list_posts,
    view= views.PostFeedView.as_view(),
    name='feed'
  ),

  path(
    route='posts/new',
    # view=views.create_post,
    view= views.CreatePostView.as_view(),
    name='create'
  ),

  path(
    route='<int:id>',
    view=views.PostDetailView.as_view(),
    name='details'
  ),
]
