from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    class RolUsuario(models.TextChoices):
        USUARIO = "usuario", "Usuario"
        ADMIN = "admin", "Administrador"

    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    rol = models.CharField(max_length=15, choices=RolUsuario.choices, default=RolUsuario.USUARIO)

    @property
    def is_usuario(self):
        return self.rol == self.RolUsuario.USUARIO

    @property
    def is_admin(self):
        return self.rol == self.RolUsuario.ADMIN

    def __str__(self):
        return self.username
