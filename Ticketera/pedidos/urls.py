
from django.urls import path,include
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    
    path("pedidos/", view=views.pedidos_repository, name="pedidos_repo"),
    path("pedidos/nuevo/", view=views.pedidos_form, name="pedidos_form"),
    path("pedidos/editar/<int:id>/", view=views.pedidos_form, name="pedidos_edit"),
    path("pedidos/eliminar/", view=views.pedidos_delete, name="pedidos_delete"),
   
]

