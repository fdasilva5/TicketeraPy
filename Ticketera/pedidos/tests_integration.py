from django.urls import reverse
from datetime import date
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from pedidos.models import Categoria, Estado, Oficina, Pedido, Tecnico

from django.contrib.auth import authenticate

User = get_user_model()

class ModelsIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_categoria_model(self):
        categoria = Categoria.objects.create(nombre='Test Categoria')
        self.assertEqual(categoria.nombre, 'Test Categoria')

    def test_estado_model(self):
        estado = Estado.objects.create(nombre='Test Estado')
        self.assertEqual(estado.nombre, 'Test Estado')

    def test_pedido_model(self):
        categoria = Categoria.objects.create(nombre='Test Categoria')
        estado = Estado.objects.create(nombre='Test Estado')
        pedido = Pedido.objects.create(comentario='Test Pedido', categoria=categoria, estado=estado, user=self.user, fechaCreacion=date.today())
        self.assertEqual(pedido.comentario, 'Test Pedido')

    def test_tecnico_model(self):
        tecnico = Tecnico.objects.create(nombre='Test Tecnico')
        self.assertEqual(tecnico.nombre, 'Test Tecnico')

class OficinaTestCase(TestCase):

    def test_must_change_password_default_value(self):
        oficina = Oficina.objects.create(username='testuser', password='12345')
        self.assertTrue(oficina.must_change_password)

class CustomPasswordChangeViewTestCase(TestCase):

    def setUp(self):
        # Creamos un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='oldpassword')

        # Iniciamos sesión como el usuario
        self.client = Client()
        self.client.login(username='testuser', password='oldpassword')

    def test_password_change_view(self):
        # Cambiamos la contraseña del usuario
        response = self.client.post(reverse('password_change'), {
            'old_password': 'oldpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        })
        # Verificamos que se redirija a la página de inicio después del cambio de contraseña
        self.assertRedirects(response, reverse('home'))

        # Verificamos que el usuario ahora pueda autenticarse con la nueva contraseña
        user = authenticate(username='testuser', password='newpassword')
        self.assertIsNotNone(user)