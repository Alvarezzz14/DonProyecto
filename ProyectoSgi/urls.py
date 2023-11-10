"""
URL configuration for ProyectoSgi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Media
from django.conf import settings
from django.conf.urls.static import static
from UsuariosSena import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.login_view, name="login_view"),
    path("dashboard/", views.homedash, name="homedash"),
    path("regUsuario/", views.registroUsuario_view, name="registroUsuario_view"),
    path("editarUsuario/<int:id>/", views.editarUsuario_view, name="editarUsuario_view"),
    path( "actualizarUsuario/<int:id>",views.actualizarUsuario_view,name="actualizarUsuario_view",),
    path("formPrestamos/", views.formPrestamos_view, name="formPrestamos_view"),
    path("formPrestamosConsumibles/",views.formPrestamosConsumibles_view,name="formPrestamosConsumibles_view",),
    path("eliminarUsuario/<int:id>/",views.eliminarUsuario_view,name="eliminarUsuario_view",),
    path("formElementos/", views.formElementos_view, name="formElementos_view"),
    path("calendario/", views.calendario, name="calendario"),
    path("consultarUsuario/", views.consultarUsuario_view, name="consultarUsuario_view"),
    path("consultarElementos/", views.consultarElementos, name="consultarElementos"),
    path("listarPrestamos/", views.listar_prestamos, name="listar_prestamos"),
    path("formElementos/", views.formElementos_view, name="formElementos_view"),
    path("listarElementos/", views.listar_elementos, name="listar_elementos"),
    path("eliminarElemento/<int:id>/", views.eliminarElemento, name="eliminarElemento"),  # eliminar registro de la base de datos desde consultar elementos
    path("generar_pdf/", views.generar_pdf, name="generar_pdf"),
    path("generar_excel/", views.generar_excel, name="generar_excel"),
    path('logout/', views.user_logout, name='logout'),
]

# Configuración para servir archivos multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
