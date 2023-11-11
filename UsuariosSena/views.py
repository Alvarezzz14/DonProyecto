from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .forms import UsuariosSenaForm, UserLoginForm, ElementosForm, PrestamosForm
from .models import UsuariosSena, Prestamo, Elementos, PrestamoConsumible
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout

# Importar biblioteca reportlab
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.units import inch

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image

# Librería excel
import xlsxwriter
from datetime import datetime
from datetime import timedelta

# Create your views here.


def login_view(request):
    if request.method == "POST":
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            numeroIdentificacion = loginForm.cleaned_data.get("numeroIdentificacion")
            password = loginForm.cleaned_data.get("password")
            user = authenticate(
                request, username=numeroIdentificacion, password=password
            )

            if user is not None:
                login(request, user)
                return redirect("homedash")

            else:
                loginForm.add_error(None, "Invalid username or password")
    else:
        loginForm = UserLoginForm()

    return render(request, "indexLogin.html", {"form": loginForm})


def homedash(request):
    return render(request, "superAdmin/basedashboard.html")


def usuariodash(request):
    return render(request, "superAdmin/usuariodash.html")

def inventariodash(request):
    return render(request, "superAdmin/inventariodash.html")


def logout(request):
    return render(request, "indexLogin.html")


def consultarUsuario_view(request):
    usuarios = UsuariosSena.objects.all()  # Consulta todos los usuarios
    return render(request, "superAdmin/consultarUsuario.html", {"usuarios": usuarios})


from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UsuariosSena

def registroUsuario_view(request):
    if request.method == "POST":
        nombresVar = request.POST.get("nombres")
        apellidosVar = request.POST.get("apellidos")
        tipoIdentificacionVar = request.POST.get("tipoIdentificacion")
        numeroIdentificacionVar = request.POST.get("numeroIdentificacion")

        # Validar si el número de identificación ya está registrado
        if UsuariosSena.objects.filter(numeroIdentificacion=numeroIdentificacionVar).exists():
            messages.error(request, "El número de identificación ya está registrado.")
        else:
            emailVar = request.POST.get("email")

            # Validar si el correo electrónico ya está registrado
            if UsuariosSena.objects.filter(email=emailVar).exists():
                messages.error(request, "El correo electrónico ya está registrado.")
            else:
                celularVar = request.POST.get("celular")
                rolVar = request.POST.get("rol")
                cuentadanteVar = request.POST.get("cuentadante")
                tipoContratoVar = request.POST.get("tipoContrato")
                is_activeVar = request.POST.get("is_active")
                duracionContratoVar = request.POST.get("duracionContrato")
                passwordVar = request.POST.get("password")
                fotoUsuarioVar = request.POST.get("fotoUsuario")

                # Crear el objeto de usuario
                user = UsuariosSena(
                    nombres=nombresVar,
                    apellidos=apellidosVar,
                    tipoIdentificacion=tipoIdentificacionVar,
                    numeroIdentificacion=numeroIdentificacionVar,
                    email=emailVar,
                    celular=celularVar,
                    rol=rolVar,
                    cuentadante=cuentadanteVar,
                    tipoContrato=tipoContratoVar,
                    is_active=is_activeVar,
                    duracionContrato=duracionContratoVar,
                    password=passwordVar,
                    fotoUsuario=fotoUsuarioVar,
                )

                # Guardar el usuario en la base de datos
                user.save()

                # Mensaje de éxito
                messages.success(request, "Usuario Registrado con Éxito")

    return render(request, "superAdmin/registroUsuario.html")



def editarUsuario_view(request, id):
    try:
        user = UsuariosSena.objects.get(id=id)
        datos = {"user": user}
        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return render(request, "superAdmin/editarUsuario.html", datos)
    except UsuariosSena.DoesNotExist:
        messages.warning(request, "No existe registro")
        return redirect("consultarUsuario_view")


def actualizarUsuario_view(request, id):
    if request.method == "POST":
        nombreVar = request.POST.get("nombre")
        apellidoVar = request.POST.get("apellidoo")
        tipoIdentificacionVar = request.POST.get("tipoIdentificacion")
        numeroIdentificacionVar = request.POST.get("numeroIdentificacion")
        correoSenaVar = request.POST.get("correoSena")
        celularVar = request.POST.get("celular")
        rolVar = request.POST.get("rol")
        cuentadanteVar = request.POST.get("cuentadante")
        tipoContratoVar = request.POST.get("tipoContrato")
        duracionContratoVar = request.POST.get("duracionContrato")
        estadoUsuariovar = request.POST.get("estadoUsuario")
        contraSenaVar = request.POST.get("contraSena")
        validacionContraSenaVar = request.POST.get("validacionContraSena")
        fotoUsuarioVar = request.FILES.get("fotoUsuario")

        user = UsuariosSena.objects.get(id=id)

        user.nombre = nombreVar
        user.apellidoo = apellidoVar
        user.tipoIdentificacion = tipoIdentificacionVar
        user.numeroIdentificacion = numeroIdentificacionVar
        user.correoSena = correoSenaVar
        user.celular = celularVar
        user.rol = rolVar
        user.cuentadante = cuentadanteVar
        user.tipoContrato = tipoContratoVar
        user.duracionContrato = duracionContratoVar
        user.estadoUsuario = estadoUsuariovar
        user.contraSena = contraSenaVar
        user.validacionContraSena = validacionContraSenaVar
        user.fotoUsuario = fotoUsuarioVar
        user.save()
        messages.success(request, "Usuario actualizado con Exito")  # mensaje de alerta

        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return redirect("consultarUsuario_view")
    else:
        messages.warning(request, "No existe registro")
        return redirect("consultarUsuario_view")


def eliminarUsuario_view(request, id):
    try:
        user = UsuariosSena.objects.get(id=id)
        user.delete()
        messages.success(
            request, "usuario eliminado correctamente"
        )  # mensaje de alerta

        user = UsuariosSena.objects.all().values()

        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return redirect("consultarUsuario_view")
    except UsuariosSena.DoesNotExist:
        messages.warning(request, "No existe registro")
        return redirect("consultarUsuario_view")


def formPrestamos_view(request):
    if request.method == "POST":
        fechaEntregaVar = request.POST.get("fechaEntrega")
        fechaDevolucionVar = request.POST.get("fechaDevolucion")
        # serialSenaElementoVar=request.POST.get('serialSenaElemento')
        # nombreVar=request.POST.get('nombre')
        observacionesPrestamoVar = request.POST.get("observacionesPrestamo")

        user = Prestamo(
            fechaEntrega=fechaEntregaVar,
            fechaDevolucion=fechaDevolucionVar,
            observacionesPrestamo=observacionesPrestamoVar,
        )
        user.save()

    return render(request, "superAdmin/formPrestamos.html")


def formPrestamosConsumibles_view(request):
    nombre_elemento = None  # Valor por defecto en caso de solicitud GET

    if request.method == "POST":
        # Procesar el formulario aquí (guardar el préstamo consumible)
        nombre_elemento = request.POST.get("nombre_elemento")
        cantidad_prestada = int(request.POST.get("cantidad_prestada"))
        fecha_entrega = request.POST.get("fecha_entrega")
        serial_elemento = request.POST.get("serial_elemento")
        nombre_solicitante = request.POST.get("nombre_solicitante")
        observaciones_prestamo = request.POST.get("observaciones_prestamo")

        # instancia de PrestamoConsumible
        prestamo_consumible = PrestamoConsumible(
            elemento_consumible=nombre_elemento,  # Asigna el elemento consumible, deberías buscarlo en la base de datos o tener una lógica para obtenerlo
            cantidad_prestada=cantidad_prestada,
            fecha_entrega=fecha_entrega,
            serial_elemento=serial_elemento,
            nombre_solicitante=nombre_solicitante,
            observaciones_prestamo=observaciones_prestamo,
        )
        # Guarda la instancia en la base de datos
        prestamo_consumible.save()

    return render(
        request,
        "superAdmin/formPrestamosConsumibles.html",
        {"nombre_elemento": nombre_elemento},
    )


def calendario(request):
    prestamos = Prestamo.objects.all()
    eventos = []

    for prestamo in prestamos:
        evento = {
            "title": prestamo.observacionesPrestamo,
            "start": prestamo.fechaEntrega.isoformat(),
            "end": (prestamo.fechaDevolucion + timedelta(days=1)).isoformat(),
        }
        eventos.append(evento)

    return render(request, "superAdmin/calendario.html", {"eventos": eventos})


def listar_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, "superAdmin/listarPrestamos.html", {"prestamos": prestamos})


def formElementos_view(request):
    if request.method == "POST":
        fechaEntregaVar = request.POST.get("fechaEntrega")
        fechaDevolucionVar = request.POST.get("fechaDevolucion")
        # serialSenaElementoVar=request.POST.get('serialSenaElemento')
        # nombreVar=request.POST.get('nombre')
        observacionesPrestamoVar = request.POST.get("observacionesPrestamo")

        user = Prestamo(
            fechaEntrega=fechaEntregaVar,
            fechaDevolucion=fechaDevolucionVar,
            observacionesPrestamo=observacionesPrestamoVar,
        )
        user.save()

    return render(request, "superAdmin/formPrestamos.html")


def formElementos_view(request):
    if request.method == "POST":
        fechaElementoVar = request.POST.get("fechaElemento")
        nombreElementoVar = request.POST.get("nombreElemento")
        categoriaElementoVar = request.POST.get("categoriaElemento")
        estadoElementoVar = request.POST.get("estadoElemento")
        cantidadElementoVar = int(request.POST.get("cantidadElemento"))
        valorUnidadElementoVar = int(request.POST.get("valorUnidadElemento"))
        valorTotalElementoVar = int(request.POST.get("valorTotalElemento"))

        serialSenaElementoVar = request.POST.get("serialSenaElemento")
        descripcionElementoVar = request.POST.get("descripcionElemento")
        observacionElementoVar = request.POST.get("observacionElemento")
        facturaElementoVar = request.POST.get("facturaElemento")

        valorTotalElementoVar = cantidadElementoVar * valorUnidadElementoVar

        elementos = Elementos(
            fechaElemento=fechaElementoVar,
            nombreElemento=nombreElementoVar,
            categoriaElemento=categoriaElementoVar,
            estadoElemento=estadoElementoVar,
            cantidadElemento=cantidadElementoVar,
            valorUnidadElemento=valorUnidadElementoVar,
            valorTotalElemento=valorTotalElementoVar,
            serialSenaElemento=serialSenaElementoVar,
            descripcionElemento=descripcionElementoVar,
            observacionElemento=observacionElementoVar,
            facturaElemento=facturaElementoVar,
        )
        elementos.save()
        messages.success(request, "Elemento Guardado Exitosamente")

    return render(request, "superAdmin/formElementos.html")


def listar_elementos(request):
    elementos = Elementos.objects.all()
    return render(request, "superAdmin/listarElemento.html", {"elementos": elementos})


def consultarElementos(request):
    elementos = Elementos.objects.all()
    return render(
        request, "superAdmin/consultarElementos.html", {"elementos": elementos}
    )


def eliminarElemento(request, id):
    try:
        # Busca el objeto con el ID especificado o devuelve un error 404 si no existe
        objeto = get_object_or_404(Elementos, id=id)

        # Realiza la eliminación del objeto
        objeto.delete()

        messages.warning(
            request, "¿Esta Seguro Que Desea Eliminar el Elemento?"
        )  # mensaje de alerta

        # Si se elimina correctamente, devuelve una respuesta JSON con un mensaje de éxito
        # response_data = {'mensaje': 'Registro eliminado correctamente'}
        # return JsonResponse(response_data)

    except Exception as e:
        # Si se produce un error, devuelve una respuesta JSON con un mensaje de error
        messages.error(request, "No se encontro el Elemento Seleccionado")

        return redirect("consultarElementos")

    return redirect("consultarElementos")


def generar_pdf(request):
    elementos = Elementos.objects.all()
    elements = []
    # Crear un objeto BytesIO para almacenar el archivo PDF generado
    buffer = BytesIO()
    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="lista_elementos_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf"'

    custom_page_size = (21.59 * inch, 27.94 * inch)

    left_margin = 1 * inch
    right_margin = 1 * inch
    top_margin = 1 * inch
    bottom_margin = 1 * inch

    # Crear el documento PDF, usando landscape para un formato apaisado
    doc = SimpleDocTemplate(
        buffer,
        pagesize=custom_page_size,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
    )

    # image_path = 'img/logo-sena-negro-png-2022.png'
    # logo = Image(image_path, width=1.5 * inch, height=1.5 * inch)  # Ajusta el ancho y alto de la imagen según tus necesidades
    # logo.hAlign = 'LEFT'  # Alinea la imagen a la izquierda

    data = [
        [
            "Fecha",
            "Nombre",
            "Categoría",
            "Estado",
            "Cantidad",
            "Valor Unidad",
            "Valor Total",
            "Descripción",
            "Observación",
            "Factura",
        ]
    ]
    for elemento in elementos:
        data.append(
            [
                elemento.fechaElemento,
                elemento.nombreElemento,
                elemento.categoriaElemento,
                elemento.estadoElemento,
                elemento.cantidadElemento,
                elemento.valorUnidadElemento,
                elemento.valorTotalElemento,
                elemento.descripcionElemento,
                elemento.observacionElemento,
                elemento.facturaElemento,
            ]
        )
    table = Table(data)

    row_style = TableStyle(
        [("BACKGROUND", (0, 0), (-1, 0), colors.grey)]
    )  # Color de fondo gris para la primera fila

    table.setStyle(row_style)
    title = "Lista de elementos"
    title_style = TableStyle(
        [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 20),  # Tamaño del título
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ]
    )
    title_data = [[title]]  # Coloca el título en una lista dentro de una lista
    title_table = Table(
        title_data, colWidths=[custom_page_size[0]]
    )  # Ancho igual al ancho de la página
    title_table.setStyle(title_style)
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.green),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    # Tamaño letra
    style = TableStyle(
        [
            ("FONTSIZE", (0, 0), (-1, -1), 16),
        ]
    )
    table.setStyle(style)

    col_widths = [
        1.5 * inch,
        1.5 * inch,
        1.5 * inch,
        1.5 * inch,
        1.0 * inch,
        1.0 * inch,
        1.0 * inch,
        2.0 * inch,
        2.0 * inch,
        1.5 * inch,
    ]
    table = Table(data, colWidths=col_widths)

    # agrega la tabla al doc. y genera PDF
    # si la ruta de la imagen está activa, agregar mediante comas 'image_path'
    elements = [title_table, table]
    doc.build(elements)

    # Obtener el valor del buffer y establecerlo como la respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def generar_excel(request):
    elementos = Elementos.objects.all()
    elements = []
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer, {"in_memory": True})
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format(
        {"bold": True, "align": "center", "valign": "vcenter", "bg_color": "gray"}
    )
    header_format.set_border(1)

    headers = [
        "Fecha",
        "Nombre",
        "Categoría",
        "Estado",
        "Cantidad",
        "Valor Unidad",
        "Valor Total",
        "Descripción",
        "Observación",
    ]

    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    # Datos de la base de datos
    for row_num, elemento in enumerate(elementos, start=1):
        worksheet.write(row_num, 0, elemento.fechaElemento)
        worksheet.write(row_num, 1, elemento.nombreElemento)
        worksheet.write(row_num, 2, elemento.categoriaElemento)
        worksheet.write(row_num, 3, elemento.estadoElemento)
        worksheet.write(row_num, 4, elemento.cantidadElemento)
        worksheet.write(row_num, 5, elemento.valorUnidadElemento)
        worksheet.write(row_num, 6, elemento.valorTotalElemento)
        worksheet.write(row_num, 7, elemento.descripcionElemento)
        worksheet.write(row_num, 8, elemento.observacionElemento)
        # worksheet.write(row_num, 9, elemento.facturaElemento)

    for col_num, header in enumerate(headers):
        worksheet.set_column(col_num, col_num, len(header) + 2)

    workbook.close()

    response = HttpResponse(content_type="application/vnd.ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="lista_elementos_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx"'
    response.write(buffer.getvalue())
    # una región temporal de memoria
    buffer.close()
    return response

def user_logout(request):
    logout(request)
    return redirect('login_view')