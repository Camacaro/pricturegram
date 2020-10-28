
# Librarias Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView

# Forms
from posts.forms import PostForm

# utiles
from datetime import datetime

# Models 
from posts.models import Post


# posts = [
#   {
#     'title': 'Mont Blac',
#     'user': {
#       'name': 'Yesica Cortes',
#       'picture': 'https://picsum.photos/id/237/60/60'
#     },
#     'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
#     'photo': 'https://picsum.photos/800/800?random=1'
#   },
#   {
#     'title': 'Alaska',
#     'user': {
#       'name': 'Inuyacha Torres',
#       'picture': 'https://picsum.photos/seed/picsum/60/60'
#     },
#     'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
#     'photo': 'https://picsum.photos/800/600?random=2'
#   },
#   {
#     'title': 'Foa',
#     'user': {
#       'name': 'Au Au',
#       'picture': 'https://picsum.photos/60/60?grayscale'
#     },
#     'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
#     'photo': 'https://picsum.photos/800/800?random=3'
#   },
# ]

# Create your views here.
def list_posts_test(request):
  content = []

  # .format(**post) es una desectruturacion para pasar las variables al template string
  for post in posts:
    content.append("""
      <p>
        <strong> {name} </strong>
      </p>
      <p>
        <small> {user} - <i> {timestamp} </i>  </small>
      </p>
      <figure>
        <img src="{picture}" />
      </figure>
    """.format(**post))

  return HttpResponse( '<br>'.join(content)  )

# este decorador lo que hace es verificar si estas logueado sino es asi te redireccionara 
# a lo que este en settings.LOGIN_URL
@login_required
def list_posts(request):

  # con el -, seria orden descendiente
  posts = Post.objects.all().order_by('-created')

  # el feed.html lo encontro ya que esta dentro de la carpeta templates
  # y en la configuracion de settings lo tenemos seteado a true para que busque
  # dentro de los directorios templates
  # https://docs.djangoproject.com/en/3.1/topics/templates/
  # return render(request, 'feed.html', {'posts': posts})
  # Ahora redirigere mis templates centralizados y que define en mi settings template dirs
  return render(request, 'posts/feed.html', {'posts': posts})

@login_required
def create_post(request):
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      # guardara el post
      form.save()
      return redirect('posts:feed')
  
  else:
    form = PostForm()

  return render(request, 'posts/new.html', {
    'form': form, 
    'profile': request.user.profile, 
    'user': request.user
  })

class PostFeedView(LoginRequiredMixin, ListView):
  '''Return all published posts.'''

  template_name = 'posts/feed.html'
  model = Post
  ordering = ('-created',)
  paginate_by = 2
  context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
  template_name='posts/detail.html'
  slug_field = 'id'
  # lo que viene en la url /<int:id> 
  slug_url_kwarg = 'id'
  queryset = Post.objects.all()
  context_object_name = 'post'

