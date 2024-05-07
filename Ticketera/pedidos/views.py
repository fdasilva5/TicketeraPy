from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Pedido,Area,Tecnico,Empleado
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, "home.html")

@login_required
def pedidos_repository(request):
    pedidos = Pedido.objects.filter(user=request.user) 
    return render(request, "pedidos/repository.html", {"pedidos": pedidos})


@login_required
def pedidos_form(request, id=None):
    errors = {}
    areas = Area.objects.all()
    empleados = Empleado.objects.all()  # Todos los empleados disponibles

    if request.method == "POST":
        pedido_id = request.POST.get("id", "")
        area_id = request.POST.get("area_id", "") 
        tecnico_id = request.POST.get("tecnico_id")
        empleado_id = request.POST.get("empleado_id", "")
        
        print("Area ID recibido:", area_id)
        print("Empleado ID recibido:", empleado_id)    
        print("tecnico",tecnico_id)
        saved = True

        if pedido_id == "":  # Si no hay ID, se crea un nuevo pedido
            saved, errors = Pedido.save_pedido({
                'comentario': request.POST.get("comentario", ""),
                'prioridad': request.POST.get("prioridad", ""),
                'area_id': request.POST.get("area_id", ""),
                'tecnico_id': request.POST.get("tecnico_id", ""),
                'empleado_id': request.POST.get("empleado_id", ""),
                'user': request.user,  
            })  
        else:  # Si hay un ID, se actualiza el pedido existente
            pedido = get_object_or_404(Pedido, pk=pedido_id)
            pedido.update_pedido(request.POST)

        if saved:
            return redirect(reverse("pedidos_repo"))

        # Renderizar el formulario nuevamente con errores
        return render(
            request, "pedidos/form.html", {
                "errors": errors,
                "areas": areas,
                "empleados": empleados,
                "pedido": request.POST,
            }
        )

    else:  # Si el método es GET
        pedido = None
        if id:  # Si se está editando un pedido existente
            pedido = get_object_or_404(Pedido, pk=id)

    return render(
        request, "pedidos/form.html", {
            "pedido": pedido,
            "areas": areas,
            "empleados": empleados,
            "errors": errors,
        }
    )

@login_required
def pedidos_delete(request):
    pedido_id = request.POST.get("pedido_id")
    pedido = get_object_or_404(Pedido, pk=int(pedido_id))
    pedido.delete()

    return redirect(reverse("pedidos_repo"))