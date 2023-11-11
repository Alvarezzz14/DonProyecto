from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

class LoginSuperStaffMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return super().dispatch(request, *args, **kwargs)
        return redirect('homedash')
    
class ValidarPermisosRequeridosUsuariosMixin(object):
    permission_required = ('usuario.registroUsuario_view', 'usuario.consultarUsuario_view',
                           'usuario.editarUsuario_view', 'usuario.actualizarUsuario_view',
                           'usuario.eliminarUsuario_view')
    url_redirect = None
    
    def get_perms(self):
        if isinstance(self.permission_required, str): return (self.permission_required)
        else:
            return self.permission_required
        
    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('login_view')
        return self.url_redirect
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'Documento eliminado.')
        return redirect(self.get_url_redirect())