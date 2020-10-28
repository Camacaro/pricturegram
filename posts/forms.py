
from django import forms

from posts.models import Post

# https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#modelform
class PostForm(forms.ModelForm):

  class Meta:
    model = Post
    fields = ['user', 'profile', 'title', 'photo']
