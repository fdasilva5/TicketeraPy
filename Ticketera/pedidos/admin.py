from django.contrib import admin
from .models import Pedido,Tecnico,Categoria,Estado

admin.site.register(Pedido)
admin.site.register(Tecnico)
admin.site.register(Categoria)
admin.site.register(Estado)

