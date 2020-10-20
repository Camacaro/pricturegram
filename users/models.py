from django.db import models
# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#extending-the-existing-user-model
from django.contrib.auth.models import User

# Create your models here.

'''
  Profile model Proxy model that extiends the base data with other infiormation
  extendiende de la clase User

  https://docs.djangoproject.com/en/3.1/ref/models/fields/#textfield
'''
class Profile(models.Model):

  # un perfil solo puede tener un usuario, y un usuario solo puede tener este perfil
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  website = models.URLField(max_length=200, blank=True)

  biography = models.TextField(blank=True)

  phone_number = models.CharField(max_length=20, blank=True)

  picture = models.ImageField(upload_to='users/pictures', blank=True, null=True )

  created = models.DateTimeField(auto_now_add=True)

  modified = models.DateTimeField(auto_now=True)

  # Esto es para la representacion del objecto para que no devuelva un Object en consola
  def __str__ (self):
    return self.user.username



