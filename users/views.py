from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# exception
from django.db.utils import IntegrityError 

# Models
from django.contrib.auth.models import User
from users.models import Profile
from posts.models import Post

# https://docs.djangoproject.com/en/3.1/topics/forms/
# https://docs.djangoproject.com/en/3.1/ref/forms/fields/
# Forms 
from users.form import ProfileForm, SignupForm

# https://docs.djangoproject.com/en/3.1/topics/auth/default/#auth-web-requests
# Create your views here.
def login_view(request):
  # import pdb; pdb.set_trace()

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
  
    user = authenticate( request, username=username, password=password )

    if user is not None:
      login(request, user)
      # feed es el nombre de la url del posts -> /
      return redirect('posts:feed')
    else:
      return render(request, 'users/login.html', {'error': 'Invalid username and password'})

  return render(request, 'users/login.html')

def signup_view(request):
  
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('users:login')
  else:
    form = SignupForm()

  return render(
    request=request,
    template_name='users/signup.html',
    context={
      'form': form
    }
  )

# Esta es sin aplicarle el Form
# def signup_view(request):
#   if request.method == 'POST':
    
#     username = request.POST['username']
#     password = request.POST['password']
#     password_confirmation = request.POST['password_confirmation']
#     first_name = request.POST['first_name']
#     last_name = request.POST['last_name']
#     email = request.POST['email']

#     if password != password_confirmation:
#       return render(request, 'users/signup.html', {'error': 'Password confirmation does not mach'} )

#     try:
#       user = User.objects.create_user(username=username, password=password)  
#       # catch un error particularmente, lo obtuve de la consola
#     except IntegrityError:
#       return render(request, 'users/signup.html', {'error': 'Username is alredy in user'} )

#     user.first_name = first_name
#     user.last_name = last_name
#     user.email = email
#     user.save()

#     # Profile
#     profile = Profile(user=user)
#     profile.save()

#     return redirect('login')

#   return render(request, 'users/signup.html')

@login_required
def update_profile(request):
  '''Update a user's profile view.'''

  profile  = request.user.profile

  if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES)
    if form.is_valid():
      data = form.cleaned_data

      profile.website = data['website']
      profile.phone_number = data['phone_number']
      profile.biography = data['biography']
      profile.picture   = data['picture']
      profile.save()

      url = reverse('users:detail', kwargs={'username': request.user.username})
      return redirect(url)
  else: 
    form = ProfileForm()

  return render(
    request=request,
    template_name='users/update_profile.html',
    context={
      'profile': profile,
      'user': request.user,
      'form': form
    }
  )

@login_required
def logout_view(request):
  logout(request)
  return redirect('users:login')

# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.detail/DetailView/
# https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#detailview

# ya no es un TemplateView sino lo vamos a pasar a un detailView
# LoginRequiredMixmin proteger la vista
class UserDetailView( LoginRequiredMixin, DetailView ):

  template_name='users/detail.html'
  # el where de la data
  slug_field = 'username'
  # lo que viene en la url /username 
  slug_url_kwarg = 'username'
  # Donde buscar la data
  queryset = User.objects.all()
  # nombre del objeto que se le manda al template
  context_object_name = 'user'

  # agregar posts al usuario del context
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.get_object()
    context["posts"] = Post.objects.filter(user=user).order_by('-created')
    return context
  
