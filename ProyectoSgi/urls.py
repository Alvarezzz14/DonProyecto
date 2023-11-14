from django.contrib import admin
from django.urls import path

# Media
from django.conf import settings
from django.conf.urls.static import static
from UsuariosSena import views
from UsuariosSena.views import get_serial_by_element_name


urlpatterns = [
    path(
        "admin/", 
        admin.site.urls
        ),
    
    path(
        "", 
        views.login_view, name="login_view"
        ),
    
    path(
        "dashboard/",
        views.homedash,
        name="homedash"
        ),
    
    path(
        "usuariodash/",
        views.usuariodash, 
        name="usuariodash"
        ),
    
    path(
        "inventariodash/",
        views.inventariodash, 
        name="inventariodash"
        ),
    
    path(
        "elementosdash/",
        views.elementosdash, 
        name="elementosdash"
        ),
    
    path(
        "regUsuario/",
        views.registroUsuario_view, 
        name="registroUsuario_view"),
    
    path(
        "editarUsuario/<int:id>/",
        views.editarUsuario_view, 
        name="editarUsuario_view"
    ),
    path(
        "actualizarUsuario/<int:id>",
        views.actualizarUsuario_view,
        name="actualizarUsuario_view",
    ),
    path(
        "formPrestamosDevolutivos/",
        views.formPrestamosDevolutivos_view,
        name="formPrestamosDevolutivos_view",
    ),
    path(
        "formPrestamosConsumibles/",
        views.formPrestamosConsumibles_view,
        name="formPrestamosConsumibles_view",
    ),
    path(
        "eliminarUsuario/<int:id>/",
        views.eliminarUsuario_view,
        name="eliminarUsuario_view",
    ),
    path(
        "formElementos/", views.formElementos_view, 
         name="formElementos_view"
    ),
    
    path("calendario/", views.calendario, name="calendario"),
    
    path
    ("consultarUsuario/",
     views.consultarUsuario_view,
     name="consultarUsuario_view"),
    
    path(
        "consultarElementos/",
        views.consultarElementos,
        name="consultarElementos"
    ),
    
    
    path("listarPrestamos/", views.listar_prestamos, name="listar_prestamos"),
    path("formElementos/", views.formElementos_view, name="formElementos_view"),
    path("listarElementos/", views.listar_elementos, name="listar_elementos"),
    path("eliminarElemento/<int:id>/", views.eliminarElemento, name="eliminarElemento"),  # eliminar registro de la base de datos desde consultar elementos
    path("generar_pdf/", views.generar_pdf, name="generar_pdf"),
    path("generar_excel/", views.generar_excel, name="generar_excel"),
    path('logout/', views.user_logout, name='logout'),
    path(
        "get-serial-by-element-name",
        get_serial_by_element_name,
        name="get_serial_by_element_name",
    ),
    path(
        "get-element-name-by-serial",
        views.get_element_name_by_serial,
        name="get-element-name-by-serial",
    ),
]

# Configuración para servir archivos multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
