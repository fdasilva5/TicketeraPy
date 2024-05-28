
from django.urls import path,include
from . import views

urlpatterns = [
    path("", view=views.home, name="home"),
    
    path("pedidos/", view=views.pedidos_repository, name="pedidos_repo"),
    path("pedidos/admin", view=views.pedidos_repository_admin, name="pedidos_repo_admin"),
    path('pedidos/historial/', views.pedidos_historial, name='pedidos_historial'), 
    path("pedidos/nuevo/", view=views.pedidos_form, name="pedidos_form"),
    path("pedidos/editar/<int:id>/", view=views.pedidos_form_admin, name="pedidos_edit"),
    path("pedidos/eliminar/", view=views.pedidos_delete, name="pedidos_delete"),
    path('send_mail/', views.send_mail_view, name='send_mail'),
]

