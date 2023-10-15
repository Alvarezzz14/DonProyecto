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
    return render(request, 'superAdmin/consultarUsuario.html')

def registroUsuario_view(request):
    
    if request.method == 'POST':
        registro_exitoso = False  # Variable de estado para el registro exitoso
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
        contraSenaVar=request.POST.get('contraSena')
        validacionContraSenaVar = request.POST.get('validacionContraSena')
        fotoUsuarioVar=request.FILES.get('fotoUsuario')

        user= UsuariosSena(nombre=nombreVar, apellidoo=apellidoVar, tipoIdentificacion=tipoIdentificacionVar, numeroIdentificacion=numeroIdentificacionVar, correoSena=correoSenaVar, celular=celularVar, rol=rolVar, cuentadante=cuentadanteVar, tipoContrato=tipoContratoVar, duracionContrato=duracionContratoVar, contraSena=contraSenaVar, validacionContraSena=validacionContraSenaVar, fotoUsuario=fotoUsuarioVar)
        user.save()
        messages.success(request,"Usuario Registrado con Exito")#mensaje de alerta
    

    return render(request, 'superAdmin/registroUsuario.html')

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
    return render(request, 'superAdmin/formElementos.html')

def listar_elementos(request):
    elementos = Elementos.objects.all()
    return render(request, 'superAdmin/listarElemento.html', {'elementos': elementos})

def consultarElementos(request):
    elementos = Elementos.objects.all()
    return render(request, 'superAdmin/consultarElementos.html', {'elementos': elementos})


def eliminar_registro(request, id):
    try:
        # Busca el objeto con el ID especificado o devuelve un error 404 si no existe
        objeto = get_object_or_404(Elementos, id=id)

        # Realiza la eliminación del objeto
        objeto.delete()

        # Si se elimina correctamente, devuelve una respuesta JSON con un mensaje de éxito
        response_data = {'mensaje': 'Registro eliminado correctamente'}
        return JsonResponse(response_data)

    except Exception as e:
        # Si se produce un error, devuelve una respuesta JSON con un mensaje de error
        response_data = {'error': str(e)}
        return JsonResponse(response_data, status=400)

