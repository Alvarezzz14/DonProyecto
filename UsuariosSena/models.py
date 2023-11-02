from django.db import models
from django.utils.html import format_html
from .choices import (
    roles,
    cuentadantes,
    estado,
    categoriaElemento,
    tipoId,
    tipoContratos,
)
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.


class UsuariosSenaManager(BaseUserManager):
    def create_user(self, numeroIdentificacion, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(numeroIdentificacion, email, password, **extra_fields)

    def create_superuser(self, numeroIdentificacion, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(numeroIdentificacion, email, password, **extra_fields)


class UsuariosSena(AbstractUser):
    nombres = models.CharField(max_length=25)
    apellidos = models.CharField(max_length=25)
    tipoIdentificacion = models.CharField(max_length=25, choices=tipoId, default="CC")
    numeroIdentificacion = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=25)
    celular = models.CharField(max_length=10)
    rol = models.CharField(max_length=25, choices=roles, default="I")
    cuentadante = models.CharField(
        max_length=25, choices=cuentadantes, default="adminD"
    )
    tipoContrato = models.CharField(max_length=25, choices=tipoContratos, default="P")
    is_active = models.BooleanField(default=1)
    duracionContrato = models.CharField(max_length=25)
    password = models.CharField(max_length=30, default="")
    fotoUsuario = models.ImageField(
        upload_to="usuarioFoto/", blank=True, null=True
    )  # Campo para la foto
    id = models.BigAutoField(primary_key=True)

    objects = UsuariosSenaManager()

    username = None
    first_name = None
    last_name = None

    # Set the node for log in
    USERNAME_FIELD = "numeroIdentificacion"


class Elementos(models.Model):
    fechaElemento = models.DateField()
    nombreElemento = models.CharField(max_length=25)
    categoriaElemento = models.CharField(
        max_length=25, choices=categoriaElemento, default="C"
    )
    estadoElemento = models.CharField(max_length=25, choices=estado, default="D")
    descripcionElemento = models.CharField(max_length=25)
    observacionElemento = models.CharField(max_length=25)

    cantidadElemento = models.IntegerField()
    valorUnidadElemento = models.IntegerField()
    valorTotalElemento = models.IntegerField()
    serialSenaElemento = models.CharField(max_length=25)
    facturaElemento = models.ImageField(
        upload_to="facturaElemento/", blank=True, null=True
    )  # Campo para la foto
    id = models.BigAutoField(primary_key=True)

    def save(self, *args, **kwargs):
        # Calcula el valor total antes de guardar el objeto en la base de datos
        self.valorTotal = self.valorUnidadElemento * self.cantidadElemento
        super(Elementos, self).save(*args, **kwargs)


class Prestamo(models.Model):
    fechaEntrega = models.DateField()
    fechaDevolucion = models.DateField()
    nombreEntrega = models.CharField(max_length=25)
    nombreRecibe = models.CharField(max_length=25, null=False)
    # serialSenaElemento = models.ForeignKey(Elementos,null=False,blank=True,on_delete=models.CASCADE)
    # nombre = models.ForeignKey(UsuariosSena,null=False,blank=True,on_delete=models.CASCADE)
    observacionesPrestamo = models.CharField(max_length=25)
    firmaDigital = models.ImageField(
        upload_to="firmaDigital/", blank=True, null=True
    )  # Campo para la foto
    id = models.BigAutoField(primary_key=True)


class SalidaConsumibles(models.Model):
    nombreEntrega = models.CharField(max_length=25)
    nombreRecibe = models.CharField(max_length=25)
    observacionesPrestamo = models.CharField(max_length=25)
    firmaDigital = models.ImageField(
        upload_to="firmaDigital/", blank=True, null=True
    )  # Campo para la foto
    id = models.BigAutoField(primary_key=True)


class PrestamoConsumible(models.Model):
    elemento_consumible = models.ForeignKey(Elementos, on_delete=models.CASCADE)
    cantidad_prestada = models.PositiveIntegerField()
    fecha_entrega = models.DateField()
    serial_elemento = models.CharField(max_length=100)
    nombre_solicitante = models.CharField(max_length=100)
    observaciones_prestamo = models.TextField()
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"Prestamo de {self.cantidad_prestada} unidades de {self.elemento_consumible.nombre}"
