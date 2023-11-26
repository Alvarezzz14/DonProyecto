from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Exists, OuterRef
from .forms import (
    UserLoginForm,
)
from .models import (
    UsuariosSena,
    Prestamo,
    InventarioDevolutivo,
    ProductosInventarioDevolutivo,
    ElementosConsumible,
    EntregaConsumible,
)
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from datetime import date


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


def logout(request):
    return render(request, "indexLogin.html")


def consultarUsuario_view(request):
    usuarios = UsuariosSena.objects.all()  # Consulta todos los usuarios
    return render(request, "superAdmin/consultarUsuario.html", {"usuarios": usuarios})


def registroUsuario_view(request):
    if request.method == "POST":
        nombresVar = request.POST.get("nombres")
        apellidosVar = request.POST.get("apellidos")
        tipoIdentificacionVar = request.POST.get("tipoIdentificacion")
        numeroIdentificacionVar = request.POST.get("numeroIdentificacion")
        emailVar = request.POST.get("email")
        celularVar = request.POST.get("celular")
        rolVar = request.POST.get("rol")
        cuentadanteVar = request.POST.get("cuentadante")
        tipoContratoVar = request.POST.get("tipoContrato")
        is_activeVar = request.POST.get("is_active")
        duracionContratoVar = request.POST.get("duracionContrato")
        passwordVar = request.POST.get("password")
        fotoUsuarioVar = request.FILES.get(
            "fotoUsuario", None
        )  # Ajustado para manejar casos en los que no se suba una foto

        # Cifrar la contraseña
        password_cifrada = make_password(passwordVar)

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
            # is_superuser=True, # puede hacer cualquier cosa
            is_staff=True,  # puede acceder al panel de administración, pero sus acciones específicas dentro del panel estarán limitadas por sus permisos asignados.
            duracionContrato=duracionContratoVar,
            password=password_cifrada,
            fotoUsuario=fotoUsuarioVar,
        )
        user.save()
        messages.success(request, "Usuario Registrado con Exito")

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


def formPrestamosDevolutivos_view(request):
    # Obtiene todos los usuarios excepto el que esta fijado de primero
    usuarios = UsuariosSena.objects.exclude(numeroIdentificacion="12345")
    # usuario específico que se quiere fijar
    try:
        usuario_pinned = UsuariosSena.objects.get(numeroIdentificacion="12345")
    except UsuariosSena.DoesNotExist:
        usuario_pinned = None

    # Obtiene el nombre del producto, el serial del inventario y los disponibles
    prestamos_activos = Prestamo.objects.filter(
        serialSenaElemento=OuterRef("pk"),
        fechaDevolucion__gte=date.today(),
    )

    elementos = (
        InventarioDevolutivo.objects.annotate(disponible=~Exists(prestamos_activos))
        .select_related("producto")
        .values_list(
            "producto__nombre", "serial", "producto__descripcion", "disponible"
        )
    )
    form_data = {}
    if request.method == "POST":
        fechaDevolucionVar = request.POST.get("fechaDevolucion")
        fechaDevolucion = date.fromisoformat(
            fechaDevolucionVar
        )  # Convierte la fecha a objeto date
        fechaEntregaVar = date.today()
        nombreEntregavar = request.POST.get("nombreEntrega")
        nombreRecibevar = request.POST.get("nombreRecibe")
        nombreElementovar = request.POST.get("nombreElemento")
        serialSenaElementovar = request.POST.get("serialSenaElemento")
        # cantidadElementoVar = int(request.POST.get("cantidadElemento"))
        valorUnidadElementoVar = int(request.POST.get("valorUnidadElemento"))
        disponiblesVar = request.POST.get("disponibles", "")

        observacionesPrestamovar = request.POST.get("observacionesPrestamo")
        form_data = {
            "fechaDevolucion": fechaDevolucionVar,
            "nombreEntrega": nombreEntregavar,
            "nombreRecibe": nombreRecibevar,
            "nombreElemento": nombreElementovar,
            "disponibles": disponiblesVar,
            "valorUnidadElemento": valorUnidadElementoVar,
            "serialSenaElemento": serialSenaElementovar,
            "observacionesPrestamo": observacionesPrestamovar,
        }
        # Dividir el nombre y apellido para nombreEntrega
        partes_nombre_entrega = nombreEntregavar.split(maxsplit=1)
        if len(partes_nombre_entrega) == 2:
            nombre_entrega, apellido_entrega = partes_nombre_entrega
        else:
            messages.error(
                request,
                "Formato inválido para el nombre del instructor que entrega. Por favor, ingrese nombre y apellido.",
            )
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {"elementos": elementos, "usuarios": usuarios},
            )

        # Dividir el nombre y apellido para nombreRecibe
        partes_nombre_recibe = nombreRecibevar.split(maxsplit=1)
        if len(partes_nombre_recibe) == 2:
            nombre_recibe, apellido_recibe = partes_nombre_recibe
        else:
            messages.error(
                request,
                "Formato inválido para el nombre del instructor que recibe. Por favor, ingrese nombre y apellido.",
            )
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {"elementos": elementos, "usuarios": usuarios},
            )
        try:
            nombreEntregaUsuario = UsuariosSena.objects.get(
                nombres=nombre_entrega, apellidos=apellido_entrega
            )
        except UsuariosSena.DoesNotExist:
            messages.error(request, "Usuario de entrega no encontrado.")
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {
                    "elementos": elementos,
                    "usuarios": usuarios,
                    "form_data": form_data,
                },
            )

        # Obtener la instancia del usuario para el campo nombreRecibe
        try:
            nombreRecibeUsuario = UsuariosSena.objects.get(
                nombres=nombre_recibe, apellidos=apellido_recibe
            )
        except UsuariosSena.DoesNotExist:
            messages.error(request, "Usuario receptor no encontrado.")
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {
                    "elementos": elementos,
                    "usuarios": usuarios,
                    "form_data": form_data,
                },
            )
        try:
            # Obtiene el inventario correspondiente al nombre del producto y serial
            inventario = InventarioDevolutivo.objects.select_related("producto").get(
                producto__nombre=nombreElementovar, serial=serialSenaElementovar
            )

            # Validaciones
            if fechaDevolucion < date.today():
                messages.error(
                    request,
                    "La fecha de devolución no puede ser anterior a la fecha actual.",
                )
                return render(
                    request,
                    "superAdmin/formPrestamosDevolutivos.html",
                    {
                        "elementos": elementos,
                        "usuarios": usuarios,
                        "form_data": form_data,
                    },
                )

            # Crea el objeto Prestamo
            prestamo = Prestamo(
                fechaEntrega=fechaEntregaVar,
                fechaDevolucion=fechaDevolucionVar,
                nombreEntrega=nombreEntregaUsuario,  # Esto es una instancia de UsuariosSena
                nombreRecibe=nombreRecibeUsuario,  # Esto tambien es una instancia de UsuariosSena
                serialSenaElemento=inventario,  # Esto es una instancia de InventarioDevolutivo
                # disponibles=disponiblesVar,
                valorUnidadElemento=valorUnidadElementoVar,
                # valorTotalElemento=valorTotalElementoVar,
                observacionesPrestamo=observacionesPrestamovar,
            )
            prestamo.save()
            # Disminuir la cantidad de elementos disponibles
            if inventario.producto.categoria == "D":
                inventario.producto.disponibles = max(
                    inventario.producto.disponibles - 1, 0
                )
                inventario.producto.save()
            messages.success(request, "Elemento Guardado Exitosamente")
            return redirect("formPrestamosDevolutivos_view")

        except InventarioDevolutivo.DoesNotExist:
            messages.error(request, "El elemento con el serial dado no existe.")
            # Renderiza de nuevo el formulario con el mensaje de error
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {
                    "elementos": elementos,
                    "usuarios": usuarios,
                    "form_data": form_data,
                },
            )
        except ValidationError as e:
            return HttpResponse(str(e), status=400)

    return render(
        request,
        "superAdmin/formPrestamosDevolutivos.html",
        {
            "elementos": elementos,
            "usuario_pinned": usuario_pinned,
            "usuarios": usuarios,
            "form_data": form_data,
        },
    )


# Rellenar Elemento
def get_element_name_by_serial(request):
    serial_number = request.GET.get("serialNumber", None)
    if serial_number:
        try:
            inventario_item = InventarioDevolutivo.objects.get(serial=serial_number)
            element_name = inventario_item.producto.nombre
            valor_unidad = inventario_item.producto.valor_unidad
            stock_disponible = inventario_item.producto.disponibles

            # Verificar si el elemento ha sido prestado
            es_prestado = Prestamo.objects.filter(
                serialSenaElemento=serial_number,
                fechaDevolucion__gte=date.today(),
            ).exists()

            return JsonResponse(
                {
                    "elementName": element_name,
                    "valorUnidad": valor_unidad,
                    "esPrestado": es_prestado,
                    "Stock": stock_disponible,
                }
            )
        except InventarioDevolutivo.DoesNotExist:
            return JsonResponse({"error": "Serial number not found"}, status=404)
    else:
        return JsonResponse({"error": "No serial number provided"}, status=400)


def formEntregasConsumibles_view(request):
    if request.method == "POST":
        # Procesar el formulario aquí (guardar el préstamo consumible)
        nombreElementovar = request.POST.get("nombreElemento")
        cantidad_prestadavar = int(request.POST.get("cantidad_prestada"))
        # fecha_entregavar = request.POST.get("fecha_entrega")
        fecha_entregavar = date.today()  # Manera 1 de hacerlo pero mas joda
        serialSenaElementovar = request.POST.get("serialSenaElemento")
        nombre_solicitantevar = request.POST.get("nombre_solicitante")
        observaciones_prestamovar = request.POST.get("observaciones_prestamo")
        responsable_Entregavar = request.POST.get("responsable_Entrega")

        # instancia de PrestamoConsumible
        prestamo_consumible = EntregaConsumible(
            nombreElemento=nombreElementovar,
            cantidad_prestada=cantidad_prestadavar,
            fecha_entrega=fecha_entregavar,
            serialSenaElemento=serialSenaElementovar,
            nombre_solicitante=nombre_solicitantevar,
            observaciones_prestamo=observaciones_prestamovar,
            responsable_Entrega=responsable_Entregavar,
        )
        # Guarda la instancia en la base de datos
        prestamo_consumible.save()
    return render(request, "superAdmin/formEntregasConsumibles.html")


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
    form_data = {}
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        categoria = request.POST.get("categoria")
        estado = request.POST.get("estado")
        descripcion = request.POST.get("descripcion")
        valor_unidad = int(request.POST.get("valor_unidad"))
        serial = request.POST.get("serial")
        observacion = request.POST.get("observacion")
        factura = request.FILES.get("factura")
        form_data = {
            "nombre": nombre,
            "valor_unidad": valor_unidad,
            "serial": serial,
            "descripcion": descripcion,
            "observacion": observacion,
        }
        if categoria == "D":  # Devolutivo
            if InventarioDevolutivo.objects.filter(serial=serial).exists():
                messages.error(
                    request,
                    "El número de serial ya está registrado para un elemento devolutivo.",
                )
                return render(
                    request, "superAdmin/formElementos.html", {"form_data": form_data}
                )
            # Verificar si el producto ya existe
            producto, created = ProductosInventarioDevolutivo.objects.get_or_create(
                nombre=nombre,
                categoria=categoria,
                estado=estado,
                descripcion=descripcion,
                valor_unidad=valor_unidad,
            )

            # Crear una nueva entrada en el Inventario Devolutivo
            InventarioDevolutivo.objects.create(
                producto=producto,
                serial=serial,
                observacion=observacion,
                factura=factura,
            )

            # Actualizar el contador de elementos disponibles
            producto.disponibles += 1
            producto.save()

            messages.success(request, "Elemento Devolutivo Guardado Exitosamente")

        elif categoria == "C":  # Consumible
            cantidad = int(request.POST.get("cantidadElemento"))
            costo_total = cantidad * valor_unidad

            # Crear un nuevo ElementosConsumible
            ElementosConsumible.objects.create(
                nombreElemento=nombre,
                categoriaElemento=categoria,
                estadoElemento=estado,
                descripcionElemento=descripcion,
                observacionElemento=observacion,
                cantidadElemento=cantidad,
                costoUnidadElemento=valor_unidad,
                costoTotalElemento=costo_total,
                facturaElemento=factura,
            )
            messages.success(request, "Elemento Consumible Guardado Exitosamente")

        else:
            messages.error(request, "Categoría de elemento no válida.")

        return redirect("formElementos_view")

    return render(request, "superAdmin/formElementos.html")


def listar_elementos(request):
    inventario = InventarioDevolutivo.objects.select_related("producto").all()
    return render(request, "superAdmin/listarElemento.html", {"inventario": inventario})


def consultarElementos(request):
    inventario = InventarioDevolutivo.objects.select_related("producto").all()
    return render(
        request, "superAdmin/consultarElementos.html", {"inventario": inventario}
    )


def eliminarElemento(request, serial):
    try:
        objeto = get_object_or_404(InventarioDevolutivo, serial=serial)
        objeto.delete()
        messages.warning(request, "¿Esta Seguro Que Desea Eliminar el Elemento?")
    except Exception as e:
        messages.error(request, "No se encontro el Elemento Seleccionado")
        return redirect("consultarElementos")
    return redirect("consultarElementos")


def generar_pdf(request):
    buffer = BytesIO()
    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="lista_elementos_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf"'

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        pagesize=(21.59 * inch, 27.94 * inch),
    )

    elementos = []
    data = [
        [
            "Fecha Registro",
            "Nombre Producto",
            "Categoría",
            "Estado",
            "Descripción",
            "Valor Unidad",
            "Serial",
            "Observación",
            "Factura",
        ]
    ]

    for inventario in InventarioDevolutivo.objects.select_related("producto").all():
        producto = inventario.producto
        data.append(
            [
                inventario.fecha_Registro.strftime("%Y-%m-%d"),
                producto.nombre,
                producto.categoria,
                producto.estado,
                producto.descripcion,
                producto.valor_unidad,
                inventario.serial,
                inventario.observacion,
                "Factura",  # Aquí puedes añadir una lógica para manejar la imagen de la factura
            ]
        )

    table = Table(data, colWidths=[1.5 * inch] * 9)
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    table.setStyle(table_style)
    elementos.append(table)
    doc.build(elementos)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def generar_excel(request):
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer, {"in_memory": True})
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format(
        {
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "bg_color": "gray",
            "border": 1,
        }
    )

    headers = [
        "Fecha Registro",
        "Nombre Producto",
        "Categoría",
        "Estado",
        "Descripción",
        "Valor Unidad",
        "Serial",
        "Observación",
    ]

    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    row_num = 1
    for inventario in InventarioDevolutivo.objects.select_related("producto").all():
        producto = inventario.producto
        worksheet.write(row_num, 0, inventario.fecha_Registro.strftime("%Y-%m-%d"))
        worksheet.write(row_num, 1, producto.nombre)
        worksheet.write(row_num, 2, producto.categoria)
        worksheet.write(row_num, 3, producto.estado)
        worksheet.write(row_num, 4, producto.descripcion)
        worksheet.write(row_num, 5, producto.valor_unidad)
        worksheet.write(row_num, 6, inventario.serial)
        worksheet.write(row_num, 7, inventario.observacion)
        row_num += 1

    for col_num, header in enumerate(headers):
        worksheet.set_column(col_num, col_num, max(len(header), 15))

    workbook.close()

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response[
        "Content-Disposition"
    ] = f'attachment; filename="lista_elementos_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx"'
    buffer.close()
    return response
