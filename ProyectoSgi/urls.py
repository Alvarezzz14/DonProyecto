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
#Media
from django.conf import settings
from django.conf.urls.static import static
from UsuariosSena import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login_view'),
    path('regUsuario/', views.registroUsuario_view, name='registroUsuario_view'),
    path('formPrestamos/', views.formPrestamos_view, name='formPrestamos_view'),
    path('formElementos/', views.formElementos_view, name='formElementos_view'),
    path('consultarUsuario/', views.consultarUsuario_view, name='consultarUsuario_view'),
    path('listarPrestamos/', views.listar_prestamos, name='listar_prestamos'),
    path('formElementos/', views.formElementos_view, name='formElementos_view'),
    path('listarElementos/', views.listar_elementos, name='listar_elementos'),

]

# Configuración para servir archivos multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
