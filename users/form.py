
from django import forms

class ProfileForm(forms.Form):
  # https://docs.djangoproject.com/en/3.1/ref/forms/fields/
  website = forms.URLField(max_length=200, required=True)

  biography = forms.CharField(max_length=500,  required=True)

  phone_number = forms.CharField(max_length=20,  required=True)

  picture = forms.ImageField()