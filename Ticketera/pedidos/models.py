from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.shortcuts import redirect


def validate_pedido(data):
    errors = {}
    comentario = data.get("comentario", "")
    categoria_id = data.get("categoria_id", "")  # Obtener el ID de la categoría

    if not comentario:
        errors["comentario"] = "Por favor ingrese un comentario"
    if not categoria_id:  # Verificar si el ID de la categoría está vacío
        errors["categoria"] = "Por favor seleccione una categoría"
    
    return errors

class Tecnico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido}".strip()  # Elimina espacios extra al inicio y al final

class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    comentario = models.CharField(max_length=100)
    comenTecnico = models.CharField(max_length=100, blank=True, null=True)
    estado = models.ForeignKey('Estado', on_delete=models.PROTECT, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pedidos")
    tecnico = models.ForeignKey('Tecnico', on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name="pedidos")
    fechaCreacion = models.DateField()

    def __str__(self):
        return self.comentario  

    @classmethod
    def save_pedido(cls, pedido_data):
        errors = validate_pedido(pedido_data)
        if errors:
            return False, errors

        try:
            estado = Estado.objects.get(id=pedido_data.get("estado_id"))
        except Estado.DoesNotExist:
            errors["estado"] = "Estado no existe"
            return False, errors

        try:
            categoria = Categoria.objects.get(id=pedido_data.get("categoria_id"))
        except Categoria.DoesNotExist:
            errors["categoria"] = "Categoria no existe"
            return False, errors

        tecnico = None
        if pedido_data.get("tecnico_id"):
            try:
                tecnico = Tecnico.objects.get(id=pedido_data.get("tecnico_id"))
            except Tecnico.DoesNotExist:
                errors["tecnico"] = "Tecnico no existe"
                return False, errors

        user = pedido_data.get("user")

        Pedido.objects.create(
            comentario=pedido_data.get("comentario"),
            fechaCreacion=pedido_data.get("fechaCreacion"),
            comenTecnico=pedido_data.get("comenTecnico"),
            estado=estado,
            categoria=categoria,
            tecnico=tecnico,
            user=user
        )

        return True, None

    def update_pedido(self, pedido_data):
        self.comentario = pedido_data.get("comentario", self.comentario)
        self.comenTecnico = pedido_data.get("comenTecnico", self.comenTecnico)

        if "tecnico_id" in pedido_data:
            tecnico_id = pedido_data.get("tecnico_id")
            if tecnico_id:
                self.tecnico = Tecnico.objects.get(id=tecnico_id)

        if "estado_id" in pedido_data:
            estado_id = pedido_data.get("estado_id")
            if estado_id:
                self.estado = Estado.objects.get(id=estado_id)

        if "categoria_id" in pedido_data:
            categoria_id = pedido_data.get("categoria_id")
            if categoria_id:
                self.categoria = Categoria.objects.get(id=categoria_id)

        self.save()


class Oficina(AbstractUser):
    must_change_password = models.BooleanField(default=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='my_groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='my_user_permissions',
        related_query_name='user',
    )