from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from pedidos.models import Categoria, Estado, Oficina, Pedido, Tecnico

User = get_user_model()

class CategoriaTestCase(TestCase):

    def test_categoria_model(self):
        categoria = Categoria.objects.create(nombre='Test Categoria')
        self.assertEqual(categoria.nombre, 'Test Categoria')

class EstadoTestCase(TestCase):

    def test_estado_model(self):
        estado = Estado.objects.create(nombre='Test Estado')
        self.assertEqual(estado.nombre, 'Test Estado')

class PedidoTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_pedido_creation(self):
        categoria = Categoria.objects.create(nombre='Test Categoria')
        estado = Estado.objects.create(nombre='Test Estado')
        pedido = Pedido.objects.create(comentario='Test Pedido', categoria=categoria, estado=estado, user=self.user, fechaCreacion=date.today())
        self.assertEqual(pedido.comentario, 'Test Pedido')


    def test_str_method(self):
        categoria = Categoria.objects.create(nombre='Test Categoria')
        estado = Estado.objects.create(nombre='Test Estado')
        pedido = Pedido.objects.create(comentario='Test Pedido', categoria=categoria, estado=estado, user=self.user, fechaCreacion=date.today())
        self.assertEqual(str(pedido), 'Test Pedido')

class TecnicoTestCase(TestCase):

    def test_tecnico_model(self):
        tecnico = Tecnico.objects.create(nombre='Test Tecnico')
        self.assertEqual(str(tecnico),'Test Tecnico')

class OficinaTestCase(TestCase):

    def test_must_change_password_default_value(self):
        oficina = Oficina.objects.create(username='testuser', password='12345')
        self.assertTrue(oficina.must_change_password)
