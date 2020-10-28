
# Django
from django.urls import path
from django.views.generic import TemplateView

# Models
from users import views


urlpatterns = [

  # Management
  path(
    route= 'login/',
    # view= views.login_view, 
    view= views.LoginView.as_view(),
    name='login'
  ),

  path(
    route= 'logout/',
    # view= views.logout_view, 
    view= views.LogoutView.as_view(),
    name='logout'
  ),

  path(
    route= 'signup/',
    # view= views.signup_view, 
    view= views.Signup.as_view(),
    name='signup'
  ),
  path(

    route= 'me/profie', 
    # view= views.update_profile, 
    view= views.UpdateProfileView.as_view(),
    name='update'
  ),

  # Posts
  # https://docs.djangoproject.com/en/3.1/topics/class-based-views/
  path(
    route= "<str:username>/",
    # view= TemplateView.as_view(template_name='users/detail.html'),
    view= views.UserDetailView.as_view(),
    name="detail"
  ),

]
