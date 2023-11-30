from django.contrib import admin
from django.urls import path, include

# Media
from django.conf import settings
from django.conf.urls.static import static
from UsuariosSena import views


from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("UsuariosSena.urls", "usu"), namespace="usu")),
    path("", views.login_view, name="login_view"),
    path("dashboard/", views.homedash, name="homedash"),
    path("usuariodash/", views.usuariodash, name="usuariodash"),
    path("inventariodash/", views.inventariodash, name="inventariodash"),
    path("elementosdash/", views.elementosdash, name="elementosdash"),
    path("transacciondash/", views.transacciondash, name="transacciondash"),
    path("regUsuario/", views.registroUsuario_view, name="registroUsuario_view"),
    path("editarUsuario/<int:numeroIdentificacion>/", views.editarUsuario_view, name="editarUsuario_view"
    ),
    
    path("editarElementoconsu/<int:id>/", views.editarElementosconsu_view, name="editarElementosconsu_view"
    ),
    
    path(
        "editarElementodevo/<int:serial>/",
        views.editarElementosdevo_view, 
        name="editarElementosdevo_view"
        
    ),
    
    path(
        "finalizarPrestamo/<int:id>/",
        views.finalizarPrestamo_view,
        name="finalizarPrestamo_view",
    ),
    path(
        "editarPrestamo/<int:id>/",
        views.editarPrestamo_view,
        name="editarPrestamo_view",
    ),
    path(
        "editarEntrega/<int:id>/", views.editarEntrega_view, name="editarEntrega_view"
    ),
    path(
        "actualizarUsuario/<int:numeroIdentificacion>",
        views.actualizarUsuario_view,
        name="actualizarUsuario_view",
    ),
    path(
        "formPrestamosDevolutivos/",
        views.formPrestamosDevolutivos_view,
        name="formPrestamosDevolutivos_view",
    ),
    path(
        "formEntregasConsumibles/",
        views.formEntregasConsumibles_view,
        name="formEntregasConsumibles_view",
    ),
    path("eliminarUsuario/<int:numeroIdentificacion>/", views.eliminarUsuario_view, name="eliminarUsuario_view",
    ),
    path("formElementos/", views.formElementos_view, name="formElementos_view"),
    path("calendario/", views.calendario, name="calendario"),
    path(
        "consultarUsuario/", views.consultarUsuario_view, name="consultarUsuario_view"
    ),
    path("consultarElementos/", views.consultarElementos, name="consultarElementos"),
    path(
        "consultarTransacciones/",
        views.consultarTransacciones_view,
        name="consultarTransacciones",
    ),
    path("formElementos/", views.formElementos_view, name="formElementos_view"),
    path("generar_pdf/", views.generar_pdf, name="generar_pdf"),
    path("generar_excel/", views.generar_excel, name="generar_excel"),
    path("logout/", views.user_logout, name="logout"),
    path(
        "get-element-name-by-serial",
        views.get_element_name_by_serial,
        name="get-element-name-by-serial",
    ),
    path(
        "get_element_consum_info/",
        views.get_element_consum_info,
        name="get_element_consum_info",
    ),
    path("reset_password/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "reset_password/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    path(
        "reporteelementosactivos/", 
        views.reporteelementosactivos, name="reporteelementosactivos"
    ),

    path(
        "reporteelementosprestamos/", 
        views.reporteelementosprestamo, name="reporteelementosprestamos"
    ),
    path(
        "reporteelementosbajas/", 
        views.reporteelementosbajas, name="reporteelementosbajas"
    ),
]

# Configuración para servir archivos multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
