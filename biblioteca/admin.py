from django.contrib import admin
from .models import Libro, Categoria


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "genero", "fecha_publicacion")
    search_fields = ("titulo", "autor")
    list_filter = ("genero", "fecha_publicacion")


admin.site.register(Categoria)
