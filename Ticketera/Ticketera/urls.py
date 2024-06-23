from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from pedidos import views
from pedidos.views import CustomPasswordChangeView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'), 
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("pedidos.urls")),
]
