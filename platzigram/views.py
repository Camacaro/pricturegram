# Django
from django.http import HttpResponse

# Utilities
import json
from datetime import datetime

def hello_world(request):
  return HttpResponse('Hello, world!')
  
def timers(request):
  # mes dia, año - hora minuta 
  now = datetime.now().strftime('%b %dth, %Y - %H:%M hrs')
  return HttpResponse('Oh, hi!  Current server time is {now}'.format(now=now) )


def sort_integers(request):
  # https://docs.djangoproject.com/en/2.0/ref/request-response/
  # imprimir en consola
  # print(request)

  # debug app en consola, puedo jugar y tomar todo lo que este de aqui para arriba
  # import pdb
  # pdb.set_trace()

  # data por params query
  numbers = request.GET['numbers']

  # list comprehension - itera y convierte en entero cada string-number del arreglo
  list_numbers = [ int(i) for i in numbers.split(',') ]

  sorted_ints = sorted(list_numbers)

  # import pdb; pdb.set_trace()

  # Esto es un diccionario - es como un objeto pero se llama diccionario
  data = {
    'status': 'ok',
    'numbers': sorted_ints,
    'message': 'Integers sorted successfully'
  }

  # traduce un diccionario a un json para retornar
  json_stringify = json.dumps(data)

  # https://docs.djangoproject.com/en/2.0/ref/request-response/#httpresponse-objects
  return HttpResponse( json_stringify, content_type='application/json' )


def say_hi(request, name, age):

  if age < 12:
    message = 'sorry {}, you are not allowed here'.format(name)
  else:
    message = 'Hell, {}! Welcome to platzigram'.format(name)

  return HttpResponse(message)