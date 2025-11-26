from django.urls import path
from .views import (
    home,
    buscar_libros,
    lista_libros,
    detalle_libro,
    crear_libro,
    editar_libro,
    eliminar_libro,
    crear_lista,
    detalle_lista,
    editar_lista,
    eliminar_lista,
    crear_reseña,
    editar_reseña,
    eliminar_reseña,
    agregar_favorito,
    quitar_favorito,
    ver_historial,
    crear_categoria,
)

urlpatterns = [
    # Home y búsqueda
    path('', home, name='homeGeneral'),
    path('buscar/', buscar_libros, name='buscar_libros'),
    path('libros/', lista_libros, name='lista_libros'),
    path('libro/<int:libro_id>/', detalle_libro, name='detalle_libro'),

    # Libros (solo admin/superuser)
    path('libro/crear/', crear_libro, name='crear_libro'),
    path('libro/<int:libro_id>/editar/', editar_libro, name='editar_libro'),
    path('libro/<int:libro_id>/eliminar/', eliminar_libro, name='eliminar_libro'),

    # Listas de usuario
    path('lista/crear/', crear_lista, name='crear_lista'),
    path('lista/<int:lista_id>/', detalle_lista, name='detalle_lista'),
    path('lista/<int:lista_id>/editar/', editar_lista, name='editar_lista'),
    path('lista/<int:lista_id>/eliminar/', eliminar_lista, name='eliminar_lista'),

    # Reseñas
    path('libro/<int:libro_id>/reseña/', crear_reseña, name='crear_reseña'),
    path('reseña/<int:reseña_id>/editar/', editar_reseña, name='editar_reseña'),
    path('reseña/<int:reseña_id>/eliminar/', eliminar_reseña, name='eliminar_reseña'),

    # Favoritos
    path('favorito/<int:libro_id>/agregar/', agregar_favorito, name='agregar_favorito'),
    path('favorito/<int:libro_id>/quitar/', quitar_favorito, name='quitar_favorito'),

    # Historial
    path('historial/', ver_historial, name='ver_historial'),

    # Categorías (solo admin/superuser)
    path('categoria/crear/', crear_categoria, name='crear_categoria'),
]
