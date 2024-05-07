from django.db import models
from django.contrib.auth.models import User


def validate_pedido(data):
    errors = {}

    comentario = data.get("comentario", "")
    prioridad = data.get("prioridad", "")
    area_id = data.get("area_id", "")
    empleado_id = data.get("empleado_id","")

    if comentario == "":
        errors["comentario"] = "Por favor ingrese un comentario"
    if prioridad == "":
        errors["prioridad"] = "Por favor ingrese la prioridad del pedido"
    if area_id == "":
        errors["area_id"] = "Por favor ingrese el area de trabajo"
    if empleado_id == "":
        errors["empleado_id"] = "Por favor ingrese el empleado que realiza el pedido"
    
    return errors



class Tecnico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

    @classmethod
    def save_tecnico(cls, tecnico_data):
        
        Tecnico.objects.create(
            nombre=tecnico_data.get("nombre"),
            apellido=tecnico_data.get("apellido")
        )

        return True, None

    def update_tecnico(self, tecnico_data):
        self.nombre = tecnico_data.get("nombre", "") or self.nombre
        self.apellido = tecnico_data.get("apellido", "") or self.apellido

        self.save()


class Area(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

    @classmethod
    def save_area(cls, area_data):
        
        Area.objects.create(
            nombre=area_data.get("area"),
        )

        return True, None

    def update_area(self, area_data):
        self.nombre = area_data.get("nombre", "") or self.nombre

        self.save()

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=15)
    area = models.ForeignKey('Area', on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre
    
   
    @classmethod
    def save_empleado(cls, empleado_data):

        area = Area.objects.get(id=empleado_data.get("area_id"))
       
        Empleado.objects.create(
            nombre=empleado_data.get("nombre"),
            apellido=empleado_data.get("apellido"),
            area=area,
        )

        return True, None

    def update_empleado(self, empleado_data):
        self.nombre = empleado_data.get("nombre", "") or self.nombre
        self.apellido = empleado_data.get("apellido", "") or self.apellido

        self.save()


class Pedido(models.Model):
    comentario = models.CharField(max_length=100)
    prioridad = models.CharField(max_length=15)
    estado = models.CharField(max_length=15,default="pendiente")
    comenTecnico = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos",blank=True)


    area = models.ForeignKey('Area', on_delete=models.PROTECT)
    tecnico = models.ForeignKey('Tecnico', on_delete=models.SET_NULL, null=True,blank=True )
    empleado = models.ForeignKey('Empleado', on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.area} {self.estado}"

    @classmethod
    def save_pedido(cls, pedido_data):
        errors = validate_pedido(pedido_data)  # Validar datos del pedido

        if len(errors):
            return False, errors

        # Obtener el área, técnico y empleado desde los datos
        area = Area.objects.get(id=pedido_data.get("area_id"))
        empleado = Empleado.objects.get(id=pedido_data.get("empleado_id"))
        user = pedido_data.get("user")
        
        if(user != area):
            return False

        # Crear el pedido
        Pedido.objects.create(
            comentario=pedido_data.get("comentario"),
            prioridad=pedido_data.get("prioridad"),
            area=area,
            empleado=empleado,
            user =user
        )

        return True, None


    # Función para actualizar un pedido existente
    def update_pedido(self, pedido_data):
        self.comentario = pedido_data.get("comentario", "") or self.comentario
        self.prioridad = pedido_data.get("prioridad", "") or self.prioridad
        self.estado = pedido_data.get("estado", "") or self.estado
        self.comenTecnico = pedido_data.get("comenTecnico", "") or self.comenTecnico
        
        if "area_id" in pedido_data:
            self.area = Area.objects.get(id=pedido_data.get("area_id")) or self.area
        if "tecnico_id" in pedido_data:
            self.tecnico = Tecnico.objects.get(id=pedido_data.get("tecnico_id")) or self.tecnico
        if "empleado_id" in pedido_data:
            self.empleado = Empleado.objects.get(id=pedido_data.get("empleado_id")) or self.empleado

        self.save()
