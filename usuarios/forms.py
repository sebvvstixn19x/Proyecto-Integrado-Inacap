from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.conf import settings


class RegistroUsuarioForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True)
    direccion = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'direccion', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.direccion = self.cleaned_data.get('direccion', '')
        user.rol = Usuario.RolUsuario.USUARIO
        if commit:
            user.save()
        return user


class RegistroAdminForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True)
    direccion = forms.CharField(max_length=150, required=False)
    admin_key = forms.CharField(
        max_length=64,
        required=True,
        help_text="Ingrese la clave de administrador"
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'direccion', 'admin_key', 'password1', 'password2']

    def clean_admin_key(self):
        clave = self.cleaned_data['admin_key']
        if clave != settings.ADMIN_KEY:
            raise forms.ValidationError("Clave de administrador incorrecta.")
        return clave

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.direccion = self.cleaned_data.get('direccion', '')
        user.rol = Usuario.RolUsuario.ADMIN
        if commit:
            user.save()
        return user
