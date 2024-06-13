# # En signals.py

# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from django.shortcuts import redirect

# @receiver(user_logged_in)
# def check_first_session(sender, user, request, **kwargs):
#     # Verificar si el usuario necesita cambiar la contraseña en su primera sesión
#     if user.must_change_password:
#         # Redirigir a la página de cambio de contraseña
#         return redirect('change_password_url_name')  # Reemplaza 'change_password_url_name' con el nombre de la URL para la página de cambio de contraseña
#     else:
#         # Redirigir a la página principal después del inicio de sesión exitoso
#         return redirect('home_url_name')  # Reemplaza 'home_url_name' con el nombre de la URL para la página principal
