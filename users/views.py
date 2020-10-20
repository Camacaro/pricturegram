from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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

@login_required
def logout_view(request):
  logout(request)
  return redirect('login')