from django.test import TestCase
import pytest
from UsuariosSena.models import *
from django.contrib.auth import get_user_model

#User test

class UsuariosSenaManagerTests(TestCase):
    
    def setUp(self):
        self.manager = UsuariosSena.objects
        
    def test_create_user(self):
        user = self.manager.create_user(
            numeroIdentificacion='1234567890',
            email='testuser@example.com',
            password='password'
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.numeroIdentificacion, '1234567890')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
    
    def test_create_superuser(self):
        superuser = self.manager.create_superuser(
            numeroIdentificacion='0987654321',
            email='admin@example.com',
            password='password'
        )
        self.assertEqual(superuser.numeroIdentificacion, '0987654321')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.check_password('password'))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

class UsuariosSenaTests(TestCase):
    
    def setUp(self):
        self.user = UsuariosSena.objects.create_user(
            numeroIdentificacion='1234567890',
            email='testuser@example.com',
            password='password',
            nombres='Test',
            apellidos='User'
        )
    
    def test_user_str(self):
        self.assertEqual(str(self.user), '1234567890')

    def test_user_has_nombres(self):
        self.assertEqual(self.user.nombres, 'Test')

    '''def test_user_email_unique(self):
        with self.assertRaises(Exception):
            UsuariosSena.objects.create_user(
                numeroIdentificacion='1234567891',
                email='testuser@example.com',
                password='password',
                nombres='Another',
                apellidos='User'
            )'''
        
#ProductoDevolutivo TEST+
class ProductosInventarioDevolutivoTests(TestCase):
    
    def setUp(self):
        self.producto = ProductosInventarioDevolutivo.objects.create(
            nombre='Producto1',
            categoria='C',
            estado='D',
            descripcion='Descripción del producto',
            valor_unidad=1000,
            disponibles=10
        )
    
    def test_producto_str(self):
        self.assertEqual(str(self.producto), 'Producto1')

class InventarioDevolutivoTests(TestCase):
    
    def setUp(self):
        self.producto = ProductosInventarioDevolutivo.objects.create(
            nombre='Producto1',
            categoria='C',
            estado='D',
            descripcion='Descripción del producto',
            valor_unidad=1000,
            disponibles=10
        )
        self.inventario = InventarioDevolutivo.objects.create(
            producto=self.producto,
            observacion='Observación',
            serial='SER123'
        )
    
    def test_inventario_str(self):
        self.assertEqual(str(self.inventario), 'SER123')


#Producto COnsumible TEST

class ProductosInventarioConsumibleTests(TestCase):
    
    def setUp(self):
        self.producto = ProductosInventarioConsumible.objects.create(
            nombreElemento='ProductoConsumible1',
            categoriaElemento='Consumible',
            estadoElemento='Disponible',
            descripcionElemento='Descripción del consumible',
            costoUnidadElemento=500,
            disponible=20
        )
    
    def test_producto_str(self):
        self.assertEqual(str(self.producto), 'ProductoConsumible1')

class InventarioConsumibleTests(TestCase):
    
    def setUp(self):
        self.producto = ProductosInventarioConsumible.objects.create(
            nombreElemento='ProductoConsumible1',
            categoriaElemento='Consumible',
            estadoElemento='Disponible',
            descripcionElemento='Descripción del consumible',
            costoUnidadElemento=500,
            disponible=20
        )
        self.inventario = InventarioConsumible.objects.create(
            productoConsumible=self.producto,
            cantidadElemento=5,
            costoTotalElemento=2500,
            observacionElemento='Observación',
        )
    
    def test_inventario_str(self):
        self.assertEqual(str(self.inventario), f"Detalle de {self.producto.nombreElemento}, Fecha de Adquisición: {self.inventario.fechaAdquisicion}")

#TEST Prestamo y EntregaCOsumible
class PrestamoTests(TestCase):
    
    def setUp(self):
        self.user = UsuariosSena.objects.create_user(
            numeroIdentificacion='1234567890',
            email='testuser@example.com',
            password='password',
            nombres='Test',
            apellidos='User'
        )
        self.producto = ProductosInventarioDevolutivo.objects.create(
            nombre='Producto1',
            categoria='C',
            estado='D',
            descripcion='Descripción del producto',
            valor_unidad=1000,
            disponibles=10
        )
        self.inventario = InventarioDevolutivo.objects.create(
            producto=self.producto,
            observacion='Observación',
            serial='SER123'
        )
        self.prestamo = Prestamo.objects.create(
            fechaEntrega='2024-07-29',
            fechaDevolucion='2024-08-29',
            nombreEntrega=self.user,
            nombreRecibe=self.user,
            serialSenaElemento=self.inventario,
            valorUnidadElemento=1000,
            observacionesPrestamo='Observaciones',
            observacionesEntrega='Observaciones de Entrega'
        )
    
    def test_prestamo_str(self):
        self.assertEqual(str(self.prestamo), f"Prestamo devolutivo del producto {self.producto.nombre}")

    def test_finalizar_prestamo(self):
        self.prestamo.finalizar_prestamo()
        self.prestamo.refresh_from_db()
        self.assertEqual(self.prestamo.estadoPrestamo, 'FINALIZADO')
        self.assertEqual(self.producto.disponibles, 11)

class EntregaConsumibleTests(TestCase):
    
    def setUp(self):
        self.user = UsuariosSena.objects.create_user(
            numeroIdentificacion='1234567890',
            email='testuser@example.com',
            password='password',
            nombres='Test',
            apellidos='User'
        )
        self.producto = ProductosInventarioConsumible.objects.create(
            nombreElemento='Consumible1',
            categoriaElemento='Consumible',
            estadoElemento='Disponible',
            descripcionElemento='Descripción del consumible',
            costoUnidadElemento=500,
            disponible=20
        )
        self.inventario = InventarioConsumible.objects.create(
            productoConsumible=self.producto,
            cantidadElemento=10,
            costoTotalElemento=5000,
            observacionElemento='Observación',
        )
        self.entrega = EntregaConsumible.objects.create(
            fecha_entrega='2024-07-29',
            responsable_Entrega=self.user,
            nombre_solicitante=self.user,
            idC=self.inventario,
            cantidad_prestada=5,
            observaciones_prestamo='Observaciones de Préstamo'
        )
        
    def test_entrega_str(self):
        self.assertEqual(self.entrega, self.entrega)


@pytest.mark.django_db
def test_create_user():
    user = UsuariosSena.objects.create_user(
        numeroIdentificacion='1234567890',
        email='testuser@example.com',
        password='password',
        nombres='Test',
        apellidos='User'
    )
    assert user.numeroIdentificacion == '1234567890'
    assert user.email == 'testuser@example.com'
    assert user.check_password('password')
    assert not user.is_superuser

@pytest.mark.django_db
def test_create_superuser():
    superuser = UsuariosSena.objects.create_superuser(
        numeroIdentificacion='0987654321',
        email='admin@example.com',
        password='password'
    )
    assert superuser.numeroIdentificacion == '0987654321'
    assert superuser.email == 'admin@example.com'
    assert superuser.check_password('password')
    assert superuser.is_superuser
    assert superuser.is_staff

@pytest.mark.django_db
def test_producto_str():
    producto = ProductosInventarioDevolutivo.objects.create(
        nombre='Producto1',
        categoria='C',
        estado='D',
        descripcion='Descripción del producto',
        valor_unidad=1000,
        disponibles=10
    )
    assert str(producto) == 'Producto1'

@pytest.mark.django_db
def test_finalizar_prestamo():
    user = UsuariosSena.objects.create_user(
        numeroIdentificacion='1234567890',
        email='testuser@example.com',
        password='password',
        nombres='Test',
        apellidos='User'
    )
    producto = ProductosInventarioDevolutivo.objects.create(
        nombre='Producto1',
        categoria='C',
        estado='D',
        descripcion='Descripción del producto',
        valor_unidad=1000,
        disponibles=10
    )
    inventario = InventarioDevolutivo.objects.create(
        producto=producto,
        observacion='Observación',
        serial='SER123'
    )
    prestamo = Prestamo.objects.create(
        fechaEntrega='2024-07-29',
        fechaDevolucion='2024-08-29',
        nombreEntrega=user,
        nombreRecibe=user,
        serialSenaElemento=inventario,
        valorUnidadElemento=1000,
        observacionesPrestamo='Observaciones',
        observacionesEntrega='Observaciones de Entrega'
    )
    prestamo.finalizar_prestamo()
    prestamo.refresh_from_db()
    producto.refresh_from_db()
    assert prestamo.estadoPrestamo == 'FINALIZADO'
    assert producto.disponibles == 11
