from django.db import models
from django.utils.html import format_html
from .choices import roles, cuentadantes, estado, categoriaElemento, tipoIdentificacion, tipoContratos, estadoUsuario


# Create your models here.
class UsuariosSena(models.Model):
    nombre = models.CharField(max_length=25)
    apellidoo = models.CharField(max_length=25)
    tipoIdentificacion = models.CharField(max_length=25,choices=tipoIdentificacion,default='CC')
    numeroIdentificacion = models.CharField(max_length=25)
    correoSena  = models.EmailField()
    celular = models.CharField(max_length=10)
    rol = models.CharField(max_length=25,choices=roles,default='I')
    cuentadante = models.CharField(max_length=25,choices=cuentadantes,default='adminD')
    tipoContrato = models.CharField(max_length=25,choices=tipoContratos,default='P')
    duracionContrato = models.CharField(max_length=25)
    estadoUsuario = models.CharField(max_length=25,choices=estadoUsuario,default='A')
    contraSena = models.CharField(max_length=25)
    validacionContraSena = models.CharField(max_length=25)
    fotoUsuario = models.ImageField(upload_to='usuarioFoto/', blank=True, null=True)  # Campo para la foto
    id = models.BigAutoField(primary_key=True)

class Elementos(models.Model):
    fechaElemento = models.DateField()
    nombreElemento = models.CharField(max_length=25)
    categoriaElemento = models.CharField(max_length=25,choices=categoriaElemento,default='C')
    estadoElemento = models.CharField(max_length=25,choices=estado,default='D')
    descripcionElemento = models.CharField(max_length=25)
    observacionElemento = models.CharField(max_length=25)

    cantidadElemento = models.IntegerField()
    valorUnidadElemento = models.IntegerField()
    valorTotalElemento = models.IntegerField()
    serialSenaElemento = models.CharField(max_length=25)
    facturaElemento = models.ImageField(upload_to='facturaElemento/', blank=True, null=True)  # Campo para la foto
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
    #serialSenaElemento = models.ForeignKey(Elementos,null=False,blank=True,on_delete=models.CASCADE)
    #nombre = models.ForeignKey(UsuariosSena,null=False,blank=True,on_delete=models.CASCADE)
    observacionesPrestamo = models.CharField(max_length=25)
    firmaDigital = models.ImageField(upload_to='firmaDigital/', blank=True, null=True)  # Campo para la foto
    id = models.BigAutoField(primary_key=True)

class SalidaConsumibles(models.Model):
    nombreEntrega = models.CharField(max_length=25)
    nombreRecibe = models.CharField(max_length=25)
    observacionesPrestamo = models.CharField(max_length=25)
    firmaDigital = models.ImageField(upload_to='firmaDigital/', blank=True, null=True)  # Campo para la foto
    id = models.BigAutoField(primary_key=True)
