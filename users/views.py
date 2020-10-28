from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView, UpdateView
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

# https://docs.djangoproject.com/en/3.1/topics/auth/default/#module-django.contrib.auth.views
class LoginView( auth_views.LoginView ):
  '''Login view'''

  template_name = 'users/login.html'
  
  # al hacer success, esto redirecciona hacia http://localhost:8000/accounts/profile/
  # para cambiar esto, se va hacia platzigram/settings y añadir
  # LOGIN_REDIRECT_URL = '/ - settings.LOGIN_REDIRECT_URL





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

# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/FormView/
# Reemplazar la funcion signup_view por una clase FormView
class Signup(FormView):
  '''Users sign up view'''
  
  template_name = 'users/signup.html'
  form_class = SignupForm
  success_url = reverse_lazy('users:login')

  def form_valid(self, form):
    '''Save for data.'''
    form.save()
    return super().form_valid(form)

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

# Actualizar formulario
# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/UpdateView/
class UpdateProfileView(LoginRequiredMixin, UpdateView):
  '''Update profile view.'''
  model = Profile
  template_name = "users/update_profile.html"
  # campos a editar
  fields = ['website', 'biography', 'phone_number', 'picture']

  def get_object(self):
    '''Return user's profile'''
    return self.request.user.profile
  
  def get_success_url(self):
    '''Return to user's profile'''
    username = self.object.user.username
    return reverse('users:detail', kwargs={'username': username} )



@login_required
def logout_view(request):
  logout(request)
  return redirect('users:login')



class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
  '''Logout view'''
  # ejemplo pero no hara nada, es el template del logout que no tiene
  template_name = 'users/logged_out.html'

  # setear la url al redirigir en settings.LOGOUT_REDIRECT_URL


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
  