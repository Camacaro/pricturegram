
from django import forms

# Models
from django.contrib.auth.models import User
from users.models import Profile

class ProfileForm(forms.Form):
  # https://docs.djangoproject.com/en/3.1/ref/forms/fields/
  website = forms.URLField(max_length=200, required=True)

  biography = forms.CharField(max_length=500,  required=True)

  phone_number = forms.CharField(max_length=20,  required=True)

  picture = forms.ImageField()

class SignupForm(forms.Form):
  # todos son requridos por defectos
  username = forms.CharField(min_length=4, max_length=50)
  # https://docs.djangoproject.com/en/3.1/ref/forms/widgets/
  password = forms.CharField(max_length=70, widget=forms.PasswordInput())

  password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput())

  first_name = forms.CharField(min_length=2, max_length=50)

  last_name = forms.CharField(min_length=2, max_length=50)

  email = forms.CharField(min_length=6, max_length=70, widget=forms.EmailInput())

  # https://docs.djangoproject.com/en/3.1/ref/forms/validation/#cleaning-a-specific-field-attribute

  # Cleaning a specific field attribute¶
  def clean_username(self): 
    # username must be unique.
    username = self.cleaned_data['username']
    # esto me regrsara un booleano si existe o no
    is_unique_usermane = User.objects.filter(username=username).exists()
    if is_unique_usermane:
      raise forms.ValidationError('Username is already in use')

    # cada vez que haga esto debo retornar el valor
    return username

  # Cleaning and validating fields that depend on each other
  def clean(self):
    # verify password confirmation match

    # llamar este metodo antes de ser sobre escritos -> super()
    data = super().clean()

    password = data['password']
    password_confirmation = data['password_confirmation']

    if password != password_confirmation:
      raise forms.ValidationError('Password do not match.')

    return data

  def save(self):
    # Crear un usuario y profile
    data = self.cleaned_data
    # sacar atributo
    data.pop('password_confirmation')
    # con el arg ** le envio todo el diccionario como el rest operator de js
    user = User.objects.create_user( **data )
    profile = Profile(user=user)
    profile.save()

