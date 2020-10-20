
# Librarias Django
from django.shortcuts import render
from django.http import HttpResponse

# utiles
from datetime import datetime


posts = [
  {
    'title': 'Mont Blac',
    'user': {
      'name': 'Yesica Cortes',
      'picture': 'https://picsum.photos/id/237/60/60'
    },
    'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
    'photo': 'https://picsum.photos/800/800?random=1'
  },
  {
    'title': 'Alaska',
    'user': {
      'name': 'Inuyacha Torres',
      'picture': 'https://picsum.photos/seed/picsum/60/60'
    },
    'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
    'photo': 'https://picsum.photos/800/600?random=2'
  },
  {
    'title': 'Foa',
    'user': {
      'name': 'Au Au',
      'picture': 'https://picsum.photos/60/60?grayscale'
    },
    'timestamp': datetime.now().strftime('%b %dth, %Y - %H:%M hrs'),
    'photo': 'https://picsum.photos/800/800?random=3'
  },
]

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

def list_posts(request):
  # el feed.html lo encontro ya que esta dentro de la carpeta templates
  # y en la configuracion de settings lo tenemos seteado a true para que busque
  # dentro de los directorios templates
  # https://docs.djangoproject.com/en/3.1/topics/templates/
  # return render(request, 'feed.html', {'posts': posts})
  # Ahora redirigere mis templates centralizados y que define en mi settings template dirs
  return render(request, 'posts/feed.html', {'posts': posts})

