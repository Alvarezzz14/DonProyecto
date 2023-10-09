# #prueba loginnnnnnnnnnnnn
# from django import forms

from django import forms
from .models import UsuariosSena, Elementos, Prestamo

class UsuariosSenaForm(forms.ModelForm):
    class Meta:
        model = UsuariosSena
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class ElementosForm(forms.ModelForm):
    class Meta:
        model = Elementos
        fields = '__all__'

class PrestamosForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = '__all__'