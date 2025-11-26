from django.urls import path
from .views import (
    registro_usuario,
    login_usuario,
    logout_usuario,
    perfil_usuario,
    editar_perfil,
    registro_admin,
)

urlpatterns = [
    # Página principal de usuarios (redirige al perfil)
    path('', perfil_usuario, name='usuarios_home'),

    # Registro de usuarios
    path('registro/', registro_usuario, name='registro'),
    path('registro_admin/', registro_admin, name='registro_admin'),

    # Autenticación
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),

    # Perfil
    path('perfil/', perfil_usuario, name='perfil'),
    path('editar/', editar_perfil, name='editar_perfil'),
]
