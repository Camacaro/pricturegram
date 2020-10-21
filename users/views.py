from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# exception
from django.db.utils import IntegrityError 

# Models
from django.contrib.auth.models import User
from users.models import Profile

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
      return redirect('feed')
    else:
      return render(request, 'users/login.html', {'error': 'Invalid username and password'})

  return render(request, 'users/login.html')

def signup_view(request):
  if request.method == 'POST':
    
    username = request.POST['username']
    password = request.POST['password']
    password_confirmation = request.POST['password_confirmation']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']

    if password != password_confirmation:
      return render(request, 'users/signup.html', {'error': 'Password confirmation does not mach'} )

    try:
      user = User.objects.create_user(username=username, password=password)  
      # catch un error particularmente, lo obtuve de la consola
    except IntegrityError:
      return render(request, 'users/signup.html', {'error': 'Username is alredy in user'} )

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()

    # Profile
    profile = Profile(user=user)
    profile.save()

    return redirect('login')

  return render(request, 'users/signup.html')

def update_profile(request):
  return render(request, 'users/update_profile.html')

@login_required
def logout_view(request):
  logout(request)
  return redirect('login')

