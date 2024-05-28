from datetime import date
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .models import Pedido,Tecnico, Categoria, Estado, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.mail import send_mail


@login_required
def send_mail_view(request):
    send_mail(
        'Nuevo pedido',
        'Hola, tenes un nuevo pedido en la ticketera',
        settings.EMAIL_HOST_USER,
        ['soporte@psico.unlp.edu.ar'],
        fail_silently=False
    )
    return redirect('home')

def admin_required(user):
    return user.is_superuser  


@login_required
def home(request):
    return render(request, "home.html")

@login_required
def pedidos_repository(request):
    categoria_id = request.GET.get('categoria_id')
    if categoria_id:
        pedidos = Pedido.objects.filter(user=request.user, categoria_id=categoria_id)
    else:
        pedidos = Pedido.objects.filter(user=request.user)

    categorias = Categoria.objects.all()

    pedidos = pedidos.order_by('-id')

    return render(request, "pedidos/repository.html", {
        "pedidos": pedidos,
        "categorias": categorias,
        "selected_categoria_id": categoria_id,
    })

@login_required
@user_passes_test(admin_required)
@user_passes_test(lambda u: u.is_superuser)
def pedidos_repository_admin(request):
    categoria_id = request.GET.get('categoria_id')
    estado_id = request.GET.get('estado_id')
    tecnico_id = request.GET.get('tecnico_id', '')
    pedido_id = request.GET.get('pedido_id')
    user_id = request.GET.get('user_id')

    pedidos = Pedido.objects.all().order_by('fechaCreacion')

    if categoria_id:
        pedidos = pedidos.filter(categoria_id=categoria_id)

    if estado_id:
        pedidos = pedidos.filter(estado_id=estado_id)

    if tecnico_id:
        if tecnico_id == "sin_tecnico":
            pedidos = pedidos.filter(tecnico_id=None)
        else:
            pedidos = pedidos.filter(tecnico_id=tecnico_id)

    if pedido_id:
        pedidos = pedidos.filter(id=pedido_id)

    if user_id:
        pedidos = pedidos.filter(user_id=user_id)
    
    pedidos = pedidos.exclude(estado__nombre__in=['Hecho', 'Sin solucion'])
    pedidos = pedidos.order_by('-id')

    categorias = Categoria.objects.all()
    estados = Estado.objects.all()
    tecnicos = Tecnico.objects.all()
    users = User.objects.all()  # Assuming 'User' is the model for users

    return render(request, "pedidosAdmin/repositoryAdmin.html", {
        "pedidos": pedidos,
        "categorias": categorias,
        "estados": estados,
        "tecnicos": tecnicos,
        "users": users,
        "selected_categoria_id": categoria_id,
        "selected_estado_id": estado_id,
        "selected_tecnico_id": tecnico_id,
        "selected_pedido_id": pedido_id,
        "selected_user_id": user_id,
    })

@login_required
@user_passes_test(admin_required)
def pedidos_historial(request):
    categoria_id = request.GET.get('categoria_id')
    estado_id = request.GET.get('estado_id')
    tecnico_id = request.GET.get('tecnico_id', '')
    pedido_id = request.GET.get('pedido_id')
    user_id = request.GET.get('user_id')

    pedidos = Pedido.objects.all().order_by('fechaCreacion')

    if categoria_id:
        pedidos = pedidos.filter(categoria_id=categoria_id)

    if estado_id:
        pedidos = pedidos.filter(estado_id=estado_id)

    if tecnico_id:
        if tecnico_id == "sin_tecnico":
            pedidos = pedidos.filter(tecnico_id=None)
        else:
            pedidos = pedidos.filter(tecnico_id=tecnico_id)

    if pedido_id:
        pedidos = pedidos.filter(id=pedido_id)

    if user_id:
        pedidos = pedidos.filter(user_id=user_id)
    
    # Incluir solo estados 'Hecho' y 'Sin solucion' para el historial
    pedidos = pedidos.filter(estado__nombre__in=['Hecho', 'Sin solucion'])
    pedidos = pedidos.order_by('-id')

    categorias = Categoria.objects.all()
    estados = Estado.objects.all()
    tecnicos = Tecnico.objects.all()
    users = User.objects.all()  # Assuming 'User' is the model for users

    return render(request, "pedidosAdmin/historialAdmin.html", {
        "pedidos": pedidos,
        "categorias": categorias,
        "estados": estados,
        "tecnicos": tecnicos,
        "users": users,
        "selected_categoria_id": categoria_id,
        "selected_estado_id": estado_id,
        "selected_tecnico_id": tecnico_id,
        "selected_pedido_id": pedido_id,
        "selected_user_id": user_id,
    })
   
@login_required
def pedidos_form(request, id=None):
    errors = {}
    saved = True
    categorias = Categoria.objects.all() #obtengo todas las categorias
    estados = Estado.objects.all() #obtengo todos los estados
    tecnicos = Tecnico.objects.all() #obtengo todos los tecnicos
    today = date.today().isoformat()

    if request.method == "POST":
        
        pedido_id = request.POST.get("id", "")

        fecha_creacion = request.POST.get('fechaCreacion')
        if not fecha_creacion:
            fecha_creacion = today
        
        pedido_data = {
            'comentario': request.POST.get("comentario", ""),
            'comen_tecnico': request.POST.get("comen_tecnico", ""),
            'fechaCreacion': fecha_creacion,
            'estado_id': request.POST.get("estado","1"),
            'categoria_id': request.POST.get("categoria","1"),
            'tecnico_id': request.POST.get("tecnico", ""),
            'user': request.user,  
        }

        if not pedido_id:  # Crear un nuevo pedido
            saved, errors = Pedido.save_pedido(pedido_data)
            if saved:  # Si el pedido se guardó correctamente, enviar el correo electrónico
                send_mail_view(request)
        else:  # Actualizar un pedido existente
            pedido = get_object_or_404(Pedido, pk=int(pedido_id))
            pedido.update_pedido(pedido_data)

        if saved:
            return redirect('pedidos_repo')

        # Renderizar el formulario nuevamente con errores
        return render(request, "pedidos/form.html", {
            "errors": errors,
            "categorias": categorias,
            "estados": estados,
            "tecnicos": tecnicos,
            "pedido": request.POST,
        })

    else:  # Si el método es GET
        pedido = None
        if id:  # Si se está editando un pedido existente
            pedido = get_object_or_404(Pedido, pk=id)

    return render(request, "pedidos/form.html", {
        "pedido": pedido,
        "categorias": categorias,
        "estados": estados,
        "tecnicos": tecnicos,
        "errors": errors,
    })

@login_required
def pedidos_form_admin(request, id=None):
    errors = {}
    categorias = Categoria.objects.all() #obtengo todas las categorias
    estados = Estado.objects.all() #obtengo todos los estados
    tecnicos = Tecnico.objects.all() #obtengo todos los tecnicos
    today = date.today().isoformat()

    if request.method == "POST":
        
        saved = True
        pedido_id = request.POST.get("id", "")

        fecha_creacion = request.POST.get('fechaCreacion')
        if not fecha_creacion:
            fecha_creacion = today
        
        pedido_data = {
            'comentario': request.POST.get("comentario", ""),
            'comenTecnico': request.POST.get("comenTecnico", ""),
            'fechaCreacion': fecha_creacion,
            'estado_id': request.POST.get("estado","1"),
            'categoria_id': request.POST.get("categoria","1"),
            'tecnico_id': request.POST.get("tecnico", ""),
            'user': request.user,  
        }

        if not pedido_id:  # Crear un nuevo pedido
            saved, errors = Pedido.save_pedido(pedido_data)
        else:  # Actualizar un pedido existente
            pedido = get_object_or_404(Pedido, pk=int(pedido_id))
            pedido.update_pedido(pedido_data)

        if saved:
            return redirect('pedidos_repo_admin')

        # Renderizar el formulario nuevamente con errores
        return render(request, "pedidosAdmin/formAdmin.html", {
            "errors": errors,
            "categorias": categorias,
            "estados": estados,
            "tecnicos": tecnicos,
            "pedido": request.POST,
        })

    else:  # Si el método es GET
        pedido = None
        if id:  # Si se está editando un pedido existente
            pedido = get_object_or_404(Pedido, pk=id)

    return render(request, "pedidosAdmin/formAdmin.html", {
        "pedido": pedido,
        "categorias": categorias,
        "estados": estados,
        "tecnicos": tecnicos,
        "errors": errors,
    })



@login_required
def pedidos_delete(request):
    
    pedido_id = request.POST.get("pedido_id")
    pedido = get_object_or_404(Pedido, pk=int(pedido_id))
    pedido.delete()

    return redirect(reverse("pedidos_repo_admin"))

