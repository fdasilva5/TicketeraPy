from django.db import models

def validate_pedido(data):
    errors = {}

    comentario = data.get("comentario", "")
    prioridad = data.get("prioridad", "")

    if comentario == "":
        errors["comentario"] = "Por favor ingrese un comentario"

    if prioridad == "":
        errors["prioridad"] = "Por favor ingrese un teléfono"


class Pedido(models.Model):
    comentario = models.CharField(max_length=100)
    prioridad = models.CharField(max_length=15)
    estado = models.EmailField()
    comenTecnico = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.comentario

    @classmethod
    def save_pedido(cls, pedido_data):
        errors = validate_pedido(pedido_data)

        if len(errors.keys()) > 0:
            return False, errors

        Pedido.objects.create(
            comentario=pedido_data.get("comentario"),
            prioridad=pedido_data.get("prioridad"),
            estado=pedido_data.get("estado"),
            comenTecnico=pedido_data.get("Comentario tecnico"),
        )

        return True, None

    def update_pedido(self, pedido_data):
        self.comentario = pedido_data.get("comentario", "") or self.comentario
        self.prioridad = pedido_data.get("prioridad", "") or self.prioridad
        self.estado = pedido_data.get("estado", "") or self.estado
        self.address = pedido_data.get("comenTecnico", "") or self.comenTecnico

        self.save()