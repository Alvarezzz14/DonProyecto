from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .forms import UsuariosSenaForm, LoginForm, ElementosForm, PrestamosForm
from .models import UsuariosSena, Prestamo, Elementos
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.

def login_view(request):
    return render(request, 'indexLogin.html')

def homedash(request):
    return render(request, 'superAdmin/basedashboard.html')

def consultarUsuario_view(request):
    usuarios = UsuariosSena.objects.all()  # Consulta todos los usuarios
    return render(request, 'superAdmin/consultarUsuario.html',{'usuarios': usuarios})

def registroUsuario_view(request):
    
    if request.method == 'POST':
        nombreVar=request.POST.get('nombre')
        apellidoVar=request.POST.get('apellidoo')
        tipoIdentificacionVar=request.POST.get('tipoIdentificacion')
        numeroIdentificacionVar=request.POST.get('numeroIdentificacion')
        correoSenaVar=request.POST.get('correoSena')
        celularVar=request.POST.get('celular')
        rolVar=request.POST.get('rol')
        cuentadanteVar=request.POST.get('cuentadante')
        tipoContratoVar=request.POST.get('tipoContrato')
        duracionContratoVar=request.POST.get('duracionContrato')
        estadoUsuarioVar=request.POST.get('estadoUsuario')
        contraSenaVar=request.POST.get('contraSena')
        validacionContraSenaVar = request.POST.get('validacionContraSena')
        fotoUsuarioVar=request.FILES.get('fotoUsuario')

        user= UsuariosSena(nombre=nombreVar, apellidoo=apellidoVar, tipoIdentificacion=tipoIdentificacionVar, numeroIdentificacion=numeroIdentificacionVar, correoSena=correoSenaVar, celular=celularVar, rol=rolVar, cuentadante=cuentadanteVar, tipoContrato=tipoContratoVar, duracionContrato=duracionContratoVar, estadoUsuario=estadoUsuarioVar, contraSena=contraSenaVar, validacionContraSena=validacionContraSenaVar, fotoUsuario=fotoUsuarioVar)
        user.save()
        messages.success(request,"Usuario Registrado con Exito")#mensaje de alerta
    

    return render(request, 'superAdmin/registroUsuario.html')

def editarUsuario_view(request, id):
    try:
        user = UsuariosSena.objects.get(id=id)
        datos = {'user': user}
         # Redirigir a la vista consultarUsuario_view para recargar los datos
        return render(request,'superAdmin/editarUsuario.html',datos)
    except UsuariosSena.DoesNotExist:
        messages.warning(request, "No existe registro")
        return redirect('consultarUsuario_view')
    

def actualizarUsuario_view(request, id):
    
    if request.method == 'POST':
        nombreVar=request.POST.get('nombre')
        apellidoVar=request.POST.get('apellidoo')
        tipoIdentificacionVar=request.POST.get('tipoIdentificacion')
        numeroIdentificacionVar=request.POST.get('numeroIdentificacion')
        correoSenaVar=request.POST.get('correoSena')
        celularVar=request.POST.get('celular')
        rolVar=request.POST.get('rol')
        cuentadanteVar=request.POST.get('cuentadante')
        tipoContratoVar=request.POST.get('tipoContrato')
        duracionContratoVar=request.POST.get('duracionContrato')
        estadoUsuariovar=request.POST.get('estadoUsuario')
        contraSenaVar=request.POST.get('contraSena')
        validacionContraSenaVar = request.POST.get('validacionContraSena')
        fotoUsuarioVar=request.FILES.get('fotoUsuario')

        user= UsuariosSena.objects.get(id = id)

        user.nombre=nombreVar 
        user.apellidoo=apellidoVar
        user.tipoIdentificacion=tipoIdentificacionVar
        user.numeroIdentificacion=numeroIdentificacionVar
        user.correoSena=correoSenaVar
        user.celular=celularVar
        user.rol=rolVar
        user.cuentadante=cuentadanteVar
        user.tipoContrato=tipoContratoVar
        user.duracionContrato=duracionContratoVar
        user.estadoUsuario=estadoUsuariovar
        user.contraSena=contraSenaVar
        user.validacionContraSena=validacionContraSenaVar
        user.fotoUsuario=fotoUsuarioVar
        user.save()
        messages.success(request,"Usuario actualizado con Exito")#mensaje de alerta

        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return redirect('consultarUsuario_view')
    else:
        messages.warning(request, "No existe registro")
        return redirect('consultarUsuario_view')
    
def eliminarUsuario_view(request, id):
    try:
        user = UsuariosSena.objects.get(id = id)
        user.delete()
        messages.success(request,"usuario eliminado correctamente")#mensaje de alerta

        user = UsuariosSena.objects.all().values()


         # Redirigir a la vista consultarUsuario_view para recargar los datos
        return redirect('consultarUsuario_view')
    except UsuariosSena.DoesNotExist:
        messages.warning(request, "No existe registro")
        return redirect('consultarUsuario_view')


def formPrestamos_view(request):
    
    if request.method == 'POST':

        fechaEntregaVar=request.POST.get('fechaEntrega')
        fechaDevolucionVar=request.POST.get('fechaDevolucion')
        #serialSenaElementoVar=request.POST.get('serialSenaElemento')
        #nombreVar=request.POST.get('nombre')
        observacionesPrestamoVar=request.POST.get('observacionesPrestamo')

        user= Prestamo(fechaEntrega=fechaEntregaVar, fechaDevolucion=fechaDevolucionVar, observacionesPrestamo=observacionesPrestamoVar)
        user.save()

    return render(request, 'superAdmin/formPrestamos.html')

def listar_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'superAdmin/listarPrestamos.html', {'prestamos': prestamos})

def formElementos_view(request):
    
    if request.method == 'POST':

        fechaEntregaVar=request.POST.get('fechaEntrega')
        fechaDevolucionVar=request.POST.get('fechaDevolucion')
        #serialSenaElementoVar=request.POST.get('serialSenaElemento')
        #nombreVar=request.POST.get('nombre')
        observacionesPrestamoVar=request.POST.get('observacionesPrestamo')

        user= Prestamo(fechaEntrega=fechaEntregaVar, fechaDevolucion=fechaDevolucionVar, observacionesPrestamo=observacionesPrestamoVar)
        user.save()

    return render(request, 'superAdmin/formPrestamos.html')


def formElementos_view(request):
    if request.method == 'POST':

        fechaElementoVar=request.POST.get('fechaElemento')
        nombreElementoVar=request.POST.get('nombreElemento')
        categoriaElementoVar=request.POST.get('categoriaElemento')
        estadoElementoVar=request.POST.get('estadoElemento')
        cantidadElementoVar=int(request.POST.get('cantidadElemento'))
        valorUnidadElementoVar=int(request.POST.get('valorUnidadElemento'))
        valorTotalElementoVar=int(request.POST.get('valorTotalElemento'))

        serialSenaElementoVar=request.POST.get('serialSenaElemento')
        descripcionElementoVar=request.POST.get('descripcionElemento')
        observacionElementoVar=request.POST.get('observacionElemento')
        facturaElementoVar=request.POST.get('facturaElemento')


        valorTotalElementoVar = cantidadElementoVar * valorUnidadElementoVar

        elementos= Elementos(fechaElemento=fechaElementoVar, nombreElemento=nombreElementoVar, categoriaElemento=categoriaElementoVar, estadoElemento=estadoElementoVar, cantidadElemento=cantidadElementoVar, valorUnidadElemento=valorUnidadElementoVar, valorTotalElemento=valorTotalElementoVar, serialSenaElemento=serialSenaElementoVar, descripcionElemento=descripcionElementoVar, observacionElemento=observacionElementoVar, facturaElemento=facturaElementoVar)
        elementos.save()
        messages.success(request,'Elemento Guardado Exitosamente')
        
    return render(request, 'superAdmin/formElementos.html')

def listar_elementos(request):
    elementos = Elementos.objects.all()
    return render(request, 'superAdmin/listarElemento.html', {'elementos': elementos})

def consultarElementos(request):
    elementos = Elementos.objects.all()
    return render(request, 'superAdmin/consultarElementos.html', {'elementos': elementos})


def eliminarElemento(request, id):
    try:
        # Busca el objeto con el ID especificado o devuelve un error 404 si no existe
        objeto = get_object_or_404(Elementos, id=id)

        # Realiza la eliminación del objeto
        objeto.delete()
        
        messages.warning(request,"¿Esta Seguro Que Desea Eliminar el Elemento?")#mensaje de alerta

        # Si se elimina correctamente, devuelve una respuesta JSON con un mensaje de éxito
        #response_data = {'mensaje': 'Registro eliminado correctamente'}
        #return JsonResponse(response_data)

    except Exception as e:
        # Si se produce un error, devuelve una respuesta JSON con un mensaje de error
        messages.error(request, "No se encontro el Elemento Seleccionado")
        
        return redirect('consultarElementos')
    
    return redirect('consultarElementos')

