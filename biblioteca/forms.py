from django import forms
from .models import Libro, Reseña, Lista, Categoria


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'descripcion', 'categoria', 'genero', 'fecha_publicacion', 'portada']


class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['comentario', 'calificacion']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


class ListaForm(forms.ModelForm):
    class Meta:
        model = Lista
        fields = ['nombre', 'descripcion', 'libros']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
        }
