
# Django
from django.shortcuts import redirect
from django.urls import reverse

# los middlewares se instalan en settings, middlewrare

# https://docs.djangoproject.com/en/3.1/topics/http/middleware/
class ProfileCompleteMiddleware:
  '''Profile completation middleware

  Ensure every user that is interacting with the platform
  have their profile picture and biography
  '''

  def __init__(self, get_response):
    self.get_response = get_response
    # One-time configuration and initialization.

  def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
    if not request.user.is_anonymous:

      # si user no es administrador
      if not request.user.is_staff:

        profile = request.user.profile

        if not profile.picture or not profile.biography:
          # si no esta / no coincide con estas dos ruta, el recerse es para encontrar el nombre de la url
          if request.path not in [reverse('update_profile'), reverse('logout')]:
            return redirect('update_profile')
    
    response = self.get_response(request)
    return response


