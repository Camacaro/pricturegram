
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Models
from users.models import Profile
from django.contrib.auth.models import User

# Register your models here.

# Se puede registar como esta abajo o como por clase, de la forma de abajo queda simple en la
# parte del admin al mostrat en la pagina 
# admin.site.register(Profile)

# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
# Decorador para registart
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

  # mostar en la lista de la tabla
  list_display = ('pk', 'user', 'phone_number', 'website', 'picture')

  # al seleccionar cualquier campo que me lleve a la descripcion del usuario
  list_display_links = ('pk', 'user')

  # poder editar desde la lista
  list_editable = ('phone_number', 'website', 'picture')

  # campo para buscar - user por ser una relacion se identifica asi el campo de el
  search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone_number')

  # lista de filtro y se refleja como los escriba el orden
  list_filter = ('created', 'modified', 'user__is_active', 'user__is_staff')

  # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
  # ordenar los campos al editar el perdil
  # fieldsets = (
  #   ('Profile', {
  #     'fields': ('user', 'picture'),
  #   }),
  # )
  fieldsets = (
    ('Profile', {
      'fields': (
        ('user', 'picture'),
      ),
    }),
    ('Extra info', {
      'fields': (
        ('website', 'phone_number'),
        ('biography')
      )
    }),
    ('Metadata', {
      'fields': (
        ('created', 'modified'),
      ),
    })
  )

  # estos campos solo seran de lectura
  readonly_fields = ('created', 'modified')

# Esta clase es para agregar el profile dentro de user al crear 
# y no tener que estar en user y luego ir a profile a crearlo,
# sino todo en una misma pantalla de user
class ProfileInline(admin.StackedInline):
  model = Profile
  can_delete = False
  verbose_name_plural = 'profiles'

# registrar inline
class UserAdmin(BaseUserAdmin):
  inlines: (ProfileInline,)

# Ahora tengo que registrar esta clase inline
admin.site.unregister(User) 
admin.site.register(User, UserAdmin)