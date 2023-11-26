from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from .choices import (
    roles,
    cuentadantes,
    estado,
    categoriaElemento,
    tipoId,
    tipoContratos,
)


class UsuariosSenaManager(BaseUserManager):
    def create_user(self, numeroIdentificacion, email, password=None, **extra_fields):
        user = self.model(
            numeroIdentificacion=numeroIdentificacion,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numeroIdentificacion, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(numeroIdentificacion, email, password, **extra_fields)


class UsuariosSena(AbstractUser):
    nombres = models.CharField(max_length=25)
    apellidos = models.CharField(max_length=25)
    tipoIdentificacion = models.CharField(max_length=25, choices=tipoId, default="CC")
    numeroIdentificacion = models.CharField(
        max_length=25, unique=True, primary_key=True
    )
    email = models.EmailField(max_length=25)
    celular = models.CharField(max_length=10)
    rol = models.CharField(max_length=25, choices=roles, default="I")
    cuentadante = models.CharField(
        max_length=25, choices=cuentadantes, default="adminD"
    )
    tipoContrato = models.CharField(max_length=25, choices=tipoContratos, default="P")
    is_active = models.BooleanField(default=1)
    duracionContrato = models.CharField(max_length=25)
    password = models.CharField(max_length=100, default="")
    fotoUsuario = models.ImageField(
        upload_to="usuarioFoto/", blank=True, null=True
    )  # Campo para la foto

    objects = UsuariosSenaManager()

    username = None
    last_name = None
    first_name = None

    # Set the node for log in
    USERNAME_FIELD = "numeroIdentificacion"


# ----Informacion General Producto (Repetitiva)---------------------------------------------------------------------------
class ProductosInventarioDevolutivo(models.Model):
    nombre = models.CharField(max_length=75)
    categoria = models.CharField(max_length=25, choices=categoriaElemento, default="C")
    estado = models.CharField(max_length=25, choices=estado, default="D")
    descripcion = models.CharField(max_length=255)
    valor_unidad = models.IntegerField()
    disponibles = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


# ----Informacion única Para El Inventario De Cada Unidad
class InventarioDevolutivo(models.Model):
    producto = models.ForeignKey(
        "ProductosInventarioDevolutivo", on_delete=models.CASCADE
    )
    fecha_Registro = models.DateField(auto_now_add=True)
    observacion = models.TextField()
    serial = models.CharField(max_length=25, primary_key=True)
    factura = models.ImageField(upload_to="facturaElemento/", blank=True, null=True)

    def __str__(self):
        return f"Serial: {self.serial} - {self.producto.nombre}"


# -------------------------------------------------------------------------------


class ElementosConsumible(models.Model):
    fechaAdquisicion = models.DateField(auto_now_add=True)
    nombreElemento = models.CharField(max_length=25)
    categoriaElemento = models.CharField(
        max_length=25, choices=[("D", "Devolutivo"), ("C", "Consumible")], default="C"
    )
    estadoElemento = models.CharField(
        max_length=25, choices=[("D", "Disponible"), ("A", "Agotado")], default="D"
    )
    descripcionElemento = models.CharField(max_length=25)
    observacionElemento = models.CharField(max_length=25)

    cantidadElemento = models.IntegerField()
    costoUnidadElemento = models.IntegerField()
    costoTotalElemento = models.IntegerField(blank=True, null=True)
    # lote = models.CharField(max_length=25)
    facturaElemento = models.ImageField(
        upload_to="facturaElemento/", blank=True, null=True
    )

    def __str__(self):
        return f"Elemento consumible {self.nombreElemento}, unidades disponibles {self.cantidadElemento}"


class Prestamo(models.Model):
    fechaEntrega = models.DateField()
    fechaDevolucion = models.DateField()
    # SE PODRIA HACER FILTRADO Y BUSCAR EN ESTE CAMPO YA SEA POR ID O NAME - IT'S OK
    nombreEntrega = models.ForeignKey(
        "UsuariosSena",
        related_name="prestamos_entregados",
        on_delete=models.SET_NULL,
        null=True,
        to_field="numeroIdentificacion",
    )
    nombreRecibe = models.ForeignKey(
        "UsuariosSena",
        related_name="prestamos_recibidos",
        on_delete=models.SET_NULL,
        null=True,
        to_field="numeroIdentificacion",
    )
    serialSenaElemento = models.ForeignKey(
        "InventarioDevolutivo", on_delete=models.CASCADE, related_name="prestamos"
    )
    # # MAS ADELANTE PROBABLEMENTE LO DEBA QUITAR
    # cantidadElemento = models.IntegerField()
    valorUnidadElemento = models.IntegerField()
    # valorTotalElemento = models.IntegerField(blank=True, null=True)
    firmaDigital = models.ImageField(upload_to="firmaDigital/", blank=True, null=True)
    observacionesPrestamo = models.TextField()

    def __str__(self):
        return f"Prestamo devolutivo de {self.cantidadElemento} unidades del producto {self.serialSenaElemento.producto.nombre}"

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"


class EntregaConsumible(models.Model):
    fecha_entrega = models.DateField()
    responsable_Entrega = models.CharField(max_length=25)
    nombre_solicitante = models.CharField(max_length=100)
    nombreElemento = models.CharField(max_length=25)
    # serialSenaElemento = models.CharField(max_length=100)
    cantidad_prestada = models.PositiveIntegerField()
    observaciones_prestamo = models.TextField()
    firmaDigital = models.ImageField(
        upload_to="firmaDigital/", blank=True, null=True
    )  # Campo para la foto
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.nombreElemento
