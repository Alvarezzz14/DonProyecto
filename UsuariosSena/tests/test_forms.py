from datetime import timezone
import pytest
from django.test import TestCase
from UsuariosSena.forms import (
    UsuariosSenaForm,
    UserLoginForm,
    PrestamosForm,
    EntregaConsumibleForm
)
from UsuariosSena.models import InventarioConsumible, InventarioDevolutivo, ProductosInventarioConsumible, ProductosInventarioDevolutivo, UsuariosSena, Prestamo, EntregaConsumible

class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UsuariosSena.objects.create_user(
            numeroIdentificacion='1234567890',
            nombres = 'Juania',
            email='testuser@example.com',
            password='password'
        )
        
        cls.productosInvDev = ProductosInventarioDevolutivo.objects.create(
            nombre = 'Laptop',
            categoria = 'C',
            estado = 'D',
            descripcion = 'akjshdkajs', 
            valor_unidad = 1200,
            disponibles = 10
        )
        
        cls.inventarioD = InventarioDevolutivo.objects.create(
            producto = cls.productosInvDev,
            observacion = 'sadas',
            serial = '128939213',
                        
        )

    @classmethod
    def tearDownClass(cls):
        cls.inventarioD.delete()
        cls.productosInvDev.delete()
        cls.user.delete()
        super().tearDownClass()

# Pruebas unitarias con unittest
class UsuariosSenaFormTest(BaseTestCase):
        
    def test_usuarios_sena_form_valid(self):
        form_data = {
            'numeroIdentificacion': '123456789100',
            'email': 'testuseerr@example.com',
            'nombres': 'Test',
            'apellidos': 'User',
            'tipoIdentificacion': 'CC',
            'celular': '1234567890',
            'rol': 'I',
            'cuentadante': 'adminD',
            'tipoContrato': 'Planta',
            'is_active': True,
            'duracionContrato': '1',
            'password': 'password' ,
            'date_joined' : '2024-01-10'
        }
       
        form = UsuariosSenaForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_usuarios_sena_form_invalid(self):
        form_data = {
            'numeroIdentificacion': '',
            'email': 'testuser@example',
        }
        form = UsuariosSenaForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

class UserLoginFormTest(BaseTestCase):
    def test_user_login_form_valid(self):
        form_data = {
            'numeroIdentificacion': self.user.numeroIdentificacion,
            'password': 'password',
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_login_form_invalid(self):
        form_data = {
            'numeroIdentificacion': '',
            'password': '',
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

class PrestamosFormTest(BaseTestCase):
    def test_prestamos_form_valid(self):
        
        form_data = {
            'nombreEntrega': self.user,
            'nombreRecibe' : self.user,
            'serialSenaElemento': self.inventarioD.serial,
            'fechaEntrega': '2024-01-01',
            'fechaDevolucion': '2024-01-10',
            'estadoPrestamo' : 'ACTIVO' ,
            'valorUnidadElemento' : '1200',
            'observacionesPrestamo' : 'asskj'
        }
        form = PrestamosForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_prestamos_form_invalid(self):
        form_data = {
             'nombreEntrega': '',
            'nombreRecibe': '',
            'estadoPrestamo' : 'ACTIVO',
            'valorUnidadElemento' : '1200',
            
        }
        form = PrestamosForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

class EntregaConsumibleFormTest(BaseTestCase):
    def test_entrega_consumible_form_valid(self):
        producto = ProductosInventarioConsumible.objects.create(
            nombreElemento='laptop',
            categoriaElemento='Consumible',
            estadoElemento='Garantia',
            descripcionElemento='ddd',
            costoUnidadElemento=2222,
            disponible=1
        )
        
        productoC = InventarioConsumible.objects.create(
            productoConsumible=producto,
            cantidadElemento=2,
            observacionElemento='asdas',            
        )
        
        form_data = {
            'responsable_Entrega': self.user.numeroIdentificacion,
            'nombreElemento': 'USB',
            'cantidad': 5,
            'fecha_entrega': '2024-01-01',
            'nombre_solicitante' :  self.user.numeroIdentificacion,
            'idC' : productoC.id,
            'cantidad_prestada': 5,
            'observaciones_prestamo': 'ussssun'
        }
        form = EntregaConsumibleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_entrega_consumible_form_invalid(self):
        form_data = {
            'nombreElemento': 'USB',
        }
        form = EntregaConsumibleForm(data=form_data)
        self.assertFalse(form.is_valid())

# Pruebas unitarias con pytest
@pytest.mark.django_db
class TestUsuariosSenaForm:
    def test_usuarios_sena_form_valid(self):
        form_data = {
            'numeroIdentificacion': '1234567890',
            'email': 'testuser@example.com',
            'nombres': 'Test',
            'apellidos': 'User',
            'tipoIdentificacion': 'CC',
            'celular': '1234567890',
            'rol': 'I',
            'cuentadante': 'adminD',
            'tipoContrato': 'Planta',
            'is_active': True,
            'duracionContrato': '1 año',
            'password': 'password',
            'date_joined': '1/1/1900'
        }
        form = UsuariosSenaForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_usuarios_sena_form_invalid(self):
        form_data = {
            'numeroIdentificacion': '',
            'email': 'testuser@example',
        }
        form = UsuariosSenaForm(data=form_data)
        assert not form.is_valid()

@pytest.mark.django_db
class TestUserLoginForm:
    def test_user_login_form_valid(self):
        form_data = {
            'numeroIdentificacion': '1234567890',
            'password': 'password',
        }
        form = UserLoginForm(data=form_data)
        assert form.is_valid()

    def test_user_login_form_invalid(self):
        form_data = {
            'numeroIdentificacion': '',
            'password': '',
        }
        form = UserLoginForm(data=form_data)
        assert not form.is_valid()

@pytest.mark.django_db
class TestPrestamosForm(BaseTestCase):
    def test_prestamos_form_valid(self):
        form_data = {
            'nombreEntrega': self.user,
            'nombreRecibe': self.user,
            'serialSenaElemento': self.inventarioD.serial,
            'fechaEntrega': '2024-01-01',
            'fechaDevolucion': '2024-01-10',
            'valorUnidadElemento' : '1200',
            'estadoPrestamo' : 'FINALIZADO',
            'observacionesPrestamo' : 'asskj'
        }
        form = PrestamosForm(data=form_data)
        assert form.is_valid(), form.errors

    def test_prestamos_form_invalid(self):
        form_data = {
            'nombreEntrega': '',
            'nombreRecibe': '',
        }
        form = PrestamosForm(data=form_data)
        assert not form.is_valid()

@pytest.mark.django_db
class TestEntregaConsumibleForm(BaseTestCase):
    def test_entrega_consumible_form_valid(self):
        producto = ProductosInventarioConsumible.objects.create(
            nombreElemento='laptop',
            categoriaElemento='Consumible',
            estadoElemento='Garantia',
            descripcionElemento='ddd',
            costoUnidadElemento=2222,
            disponible=1
        )
        
        productoC = InventarioConsumible.objects.create(
            productoConsumible=producto,
            cantidadElemento=2,
            observacionElemento='asdas',            
        )
        
        form_data = {
            'fecha_entrega': '2024-01-01',
            'responsable_Entrega': self.user.numeroIdentificacion,
            'nombre_solicitante': self.user.numeroIdentificacion,
            'idC': productoC.id,
            'cantidad_prestada': 5,
            'observaciones_prestamo': 'ussssun'
        }
        form = EntregaConsumibleForm(data=form_data)
        assert form.is_valid()

    def test_entrega_consumible_form_invalid(self):
        form_data = {
            'nombreElemento': 'USB',
        }
        form = EntregaConsumibleForm(data=form_data)
        assert not form.is_valid()