from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Pedido,Tecnico,Categoria,Estado, Oficina

admin.site.register(Oficina, UserAdmin)


admin.site.register(Pedido)
admin.site.register(Tecnico)
admin.site.register(Categoria)
admin.site.register(Estado)
