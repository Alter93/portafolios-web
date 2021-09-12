from django.contrib import admin
from portfolios.models import Usuario, Comentario, Portafolio, UsuarioPortafolio

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Comentario)
admin.site.register(Portafolio)
admin.site.register(UsuarioPortafolio)
