from django.urls import reverse
from datetime import date
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Tecnico, Estado, Categoria, Pedido, validate_pedido
from .views import send_mail_view, home, pedidos_repository, pedidos_repository_admin, pedidos_historial, pedidos_form, pedidos_form_admin, pedidos_delete

from django.contrib.auth.models import User

class ModelsIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.estado = Estado.objects.create(nombre='Estado de prueba')
        self.tecnico = Tecnico.objects.create(nombre='Nombre', apellido='Apellido')
        self.categoria = Categoria.objects.create(nombre='Categoria de prueba')
        self.pedido = Pedido.objects.create(comentario='Comentario de prueba', estado=self.estado, user=self.user, tecnico=self.tecnico, categoria=self.categoria, fechaCreacion='2024-06-10')

    def test_validate_pedido(self):
        # Caso de prueba: Comentario vacío
        data = {'comentario': '', 'categoria_id': 1}
        errors = validate_pedido(data)
        self.assertTrue('comentario' in errors)

        # Caso de prueba: Categoría vacía
        data = {'comentario': 'Comentario', 'categoria_id': ''}
        errors = validate_pedido(data)
        self.assertTrue('categoria' in errors)

        # Caso de prueba: Datos válidos
        data = {'comentario': 'Comentario', 'categoria_id': 1}
        errors = validate_pedido(data)
        self.assertFalse(errors)

    def test_pedido_model(self):
        pedido = Pedido.objects.get(id=1)
        self.assertEqual(pedido.comentario, 'Comentario de prueba')

    def test_tecnico_model(self):
        tecnico = Tecnico.objects.get(id=1)
        self.assertEqual(tecnico.nombre, 'Nombre')

    def test_estado_model(self):
        estado = Estado.objects.get(id=1)
        self.assertEqual(estado.nombre, 'Estado de prueba')

    def test_categoria_model(self):
        categoria = Categoria.objects.get(id=1)
        self.assertEqual(categoria.nombre, 'Categoria de prueba')

    def test_save_pedido(self):
        # Caso de prueba: Datos inválidos
        pedido_data = {'comentario': '', 'estado_id': 1, 'categoria_id': 1, 'user': self.user}
        success, errors = Pedido.save_pedido(pedido_data)
        self.assertFalse(success)
        self.assertTrue(errors)

        # Caso de prueba: Datos válidos
        pedido_data = {'comentario': 'Nuevo comentario', 'estado_id': 1, 'categoria_id': 1, 'user': self.user, 'fechaCreacion': '2024-06-10'}
        success, errors = Pedido.save_pedido(pedido_data)
        self.assertTrue(success)
        self.assertIsNone(errors)

    def test_update_pedido(self):
        # Caso de prueba: Actualización de comentario
        pedido_data = {'comentario': 'Nuevo comentario'}
        self.pedido.update_pedido(pedido_data)
        self.assertEqual(self.pedido.comentario, 'Nuevo comentario')

        # Caso de prueba: Actualización de técnico
        tecnico = Tecnico.objects.create(nombre='Nuevo nombre', apellido='Nuevo apellido')
        pedido_data = {'tecnico_id': tecnico.id}
        self.pedido.update_pedido(pedido_data)
        self.assertEqual(self.pedido.tecnico.nombre, 'Nuevo nombre')

        # Caso de prueba: Actualización de estado
        estado = Estado.objects.create(nombre='Nuevo estado')
        pedido_data = {'estado_id': estado.id}
        self.pedido.update_pedido(pedido_data)
        self.assertEqual(self.pedido.estado.nombre, 'Nuevo estado')

        # Caso de prueba: Actualización de categoría
        categoria = Categoria.objects.create(nombre='Nueva categoría')
        pedido_data = {'categoria_id': categoria.id}
        self.pedido.update_pedido(pedido_data)
        self.assertEqual(self.pedido.categoria.nombre, 'Nueva categoría')

class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.categoria = Categoria.objects.create(nombre='Categoria Test')
        self.estado = Estado.objects.create(nombre='Estado Test')
        self.tecnico = Tecnico.objects.create(nombre='Tecnico Test')
        self.pedido = Pedido.objects.create(
        comentario='Comentario de prueba',
        fechaCreacion=date.today(),
        estado=self.estado,
        categoria=self.categoria,
        tecnico=self.tecnico,
        user=self.user
    )
        
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_pedidos_repository_view(self):
        response = self.client.get(reverse('pedidos_repo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pedidos/repository.html')

 