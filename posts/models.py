# django
from django.db import models

# Create your models here.

# hereda model.Modes
class User(models.Model):

  email: models.EmailField( unique=True )
  password: models.CharField( max_length=100 )

  first_name: models.CharField( max_length=100 )
  last_name = models.CharField( max_length=100 )

  is_admin = models.BooleanField(default=False)

  bio = models.TextField(blank=True)
  
  # solo fecha
  birthdate = models.DateField(blank=True, null=True)

  # fecha y hora
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)