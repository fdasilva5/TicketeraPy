from datetime import date
from threading import Thread
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Oficina, Pedido,Tecnico, Categoria, Estado
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash



#Enviar mail en segundo plano
def send_mail_thread(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

#Enviar de mail luego de que un usuario realice un nuevo pedido 
@login_required
def send_mail_view(request):
    subject = 'Nuevo pedido'
    message = 'Hola, tenes un nuevo pedido en la ticketera'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['fdasilva@psico.unlp.edu.ar']
    
    #Ejecuta el envio de mail en segundo plano
    email_thread = Thread(target=send_mail_thread, args=(subject, message, from_email, recipient_list))
    email_thread.start()
    
    return redirect('home')

def admin_required(user):
    return user.is_superuser  

#Clase para gestionar el cambio de contraseña al iniciar sesion por primera vez 
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Cambiar el estado de must_change_password a False
        self.request.user.must_change_password = False
        self.request.user.save()
        # Actualizar la sesión del usuario para que no se cierre después del cambio de contraseña
        update_session_auth_hash(self.request, self.request.user)
        return super().form_valid(form)

#Home con condicion para primer inicio de sesion 
@login_required
def home(request):
    user = request.user
    if user.is_authenticated and user.must_change_password:
        return redirect('password_change/')
    else:
        return render(request, "home.html") 

#Mostrar pedidos del usuario logueado 
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


#Mostrar pedidos de todos los usuarios solo al admin
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
    users = Oficina.objects.all()  # Assuming 'User' is the model for users
    
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

#Historial de todos los pedidos, admin 
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
    users = Oficina.objects.all()  # Assuming 'User' is the model for users

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
   
#Formulario de pedidos usuarios general
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

#Formularios de pedidos admin, puede modificar
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


#Eliminar pedido
@login_required
def pedidos_delete(request):
    
    pedido_id = request.POST.get("pedido_id")
    pedido = get_object_or_404(Pedido, pk=int(pedido_id))
    pedido.delete()

    return redirect(reverse("pedidos_repo_admin"))

