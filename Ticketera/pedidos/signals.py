from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect
from .models import Oficina


@receiver(user_logged_in)
def handle_user_logged_in(sender, request, user, **kwargs):
    if isinstance(user, Oficina) and user.must_change_password:
        return redirect('password_change')