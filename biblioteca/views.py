from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import ListaForm, ReseñaForm, LibroForm, CategoriaForm
from .models import Libro, Reseña, Favorito, Historial, Lista


# -------------------------------
# Crear libro (solo admin o superusuario)
# -------------------------------
@login_required
def crear_libro(request):
    if not request.user.is_superuser and getattr(request.user, "rol", None) != "admin":
        return redirect("homeGeneral")

    if request.method == "POST":
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "El libro se agregó correctamente.")
            return redirect("lista_libros")
    else:
        form = LibroForm()

    return render(request, "biblioteca/crear_libro.html", {"form": form})


# -------------------------------
# Editar libro (solo admin)
# -------------------------------
@login_required
def editar_libro(request, libro_id):
    if request.user.rol != "admin":
        return redirect('homeGeneral')

    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, "Libro actualizado correctamente.")
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'biblioteca/editar_libro.html', {'form': form, 'libro': libro})


# -------------------------------
# Eliminar libro (solo admin)
# -------------------------------
@login_required
def eliminar_libro(request, libro_id):
    if request.user.rol != "admin":
        return redirect('homeGeneral')

    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        libro.delete()
        messages.success(request, "Libro eliminado correctamente.")
        return redirect('lista_libros')

    return render(request, 'biblioteca/eliminar_libro.html', {'libro': libro})


# -------------------------------
# Home y búsqueda
# -------------------------------
def home(request):
    libros_destacados = Libro.objects.all()[:3]
    libros_recientes = Libro.objects.order_by('-id')[:6]

    categorias = [
        "Todos",
        "Romance",
        "Ciencia ficción",
        "Fantasía",
        "Cómics",
        "Misterio",
        "Historia"
    ]

    return render(request, 'biblioteca/home.html', {
        'libros_destacados': libros_destacados,
        'libros_recientes': libros_recientes,
        'categorias': categorias
    })


def buscar_libros(request):
    query = request.GET.get('q')
    resultados = Libro.objects.all()

    if query:
        resultados = resultados.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(genero__icontains=query)
        )

    return render(request, 'biblioteca/buscar_libros.html', {
        'resultados': resultados,
        'query': query
    })


def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'biblioteca/lista_libros.html', {'libros': libros})


# -------------------------------
# Listas de usuario
# -------------------------------
@login_required
def crear_lista(request):
    if request.method == 'POST':
        form = ListaForm(request.POST)
        if form.is_valid():
            lista = form.save(commit=False)
            lista.usuario = request.user
            lista.save()
            form.save_m2m()
            return redirect('perfil')
    else:
        form = ListaForm()
    return render(request, 'biblioteca/crear_lista.html', {'form': form})


@login_required
def detalle_lista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id, usuario=request.user)
    return render(request, 'biblioteca/detalle_lista.html', {'lista': lista})


@login_required
def editar_lista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id, usuario=request.user)
    if request.method == 'POST':
        form = ListaForm(request.POST, instance=lista)
        if form.is_valid():
            form.save()
            messages.success(request, "La lista se actualizó correctamente.")
            return redirect('perfil')
    else:
        form = ListaForm(instance=lista)
    return render(request, 'biblioteca/editar_lista.html', {'form': form, 'lista': lista})


@login_required
def eliminar_lista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id, usuario=request.user)
    if request.method == 'POST':
        lista.delete()
        messages.success(request, "La lista se eliminó correctamente.")
        return redirect('perfil')
    return render(request, 'biblioteca/eliminar_lista.html', {'lista': lista})


# -------------------------------
# Libros y reseñas
# -------------------------------
@login_required
def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.user.is_authenticated and getattr(request.user, "is_usuario", False):
        Historial.objects.create(usuario=request.user, libro=libro)

    reseñas = Reseña.objects.filter(libro=libro)

    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(usuario=request.user, libro=libro).exists()

    return render(request, 'biblioteca/detalle_libro.html', {
        'libro': libro,
        'reseñas': reseñas,
        'es_favorito': es_favorito
    })


@login_required
def crear_reseña(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if not getattr(request.user, "is_usuario", False):
        return redirect('homeGeneral')

    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        calificacion = request.POST.get('calificacion')
        Reseña.objects.create(
            usuario=request.user,
            libro=libro,
            comentario=comentario,
            calificacion=calificacion
        )
        return HttpResponseRedirect(reverse('detalle_libro', args=[libro.id]))

    return render(request, 'biblioteca/reseña_form.html', {'libro': libro})


@login_required
def editar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id, usuario=request.user)
    if request.method == 'POST':
        form = ReseñaForm(request.POST, instance=reseña)
        if form.is_valid():
            form.save()
            messages.success(request, "La reseña se actualizó correctamente.")
            return redirect('perfil')
    else:
        form = ReseñaForm(instance=reseña)
    return render(request, 'biblioteca/editar_reseña.html', {'form': form, 'reseña': reseña})


@login_required
def eliminar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id, usuario=request.user)
    if request.method == 'POST':
        reseña.delete()
        messages.success(request, "La reseña se eliminó correctamente.")
        return redirect('perfil')
    return render(request, 'biblioteca/eliminar_reseña.html', {'reseña': reseña})


# -------------------------------
# Favoritos
# -------------------------------
@login_required
def agregar_favorito(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    Favorito.objects.get_or_create(usuario=request.user, libro=libro)
    return redirect('detalle_libro', libro_id=libro.id)


@login_required
def quitar_favorito(request, libro_id):
    favorito = get_object_or_404(Favorito, usuario=request.user, libro_id=libro_id)
    if request.method == 'POST':
        favorito.delete()
        messages.success(request, "El libro se quitó de tus favoritos.")
        return redirect('perfil')
    return render(request, 'biblioteca/quitar_favorito.html', {'favorito': favorito})


# -------------------------------
# Historial
# -------------------------------
@login_required
def ver_historial(request):
    historial = Historial.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'biblioteca/historial.html', {'historial': historial})


# -------------------------------
# Categorías (solo admin o superusuario)
# -------------------------------
@login_required
def crear_categoria(request):
    if not request.user.is_superuser and getattr(request.user, "rol", None) != "admin":
        return redirect("homeGeneral")

    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect("homeGeneral")
    else:
        form = CategoriaForm()

    return render(request, "biblioteca/crear_categoria.html", {"form": form})


# -------------------------------
# Perfil de usuario
# -------------------------------
@login_required
def perfil(request):
    reseñas = Reseña.objects.filter(usuario=request.user).order_by('-fecha')
    favoritos = Favorito.objects.filter(usuario=request.user)
    listas = Lista.objects.filter(usuario=request.user)
    historial = Historial.objects.filter(usuario=request.user).order_by('-fecha')

    return render(request, 'usuarios/perfil.html', {
        'reseñas': reseñas,
        'favoritos': favoritos,
        'listas': listas,
        'historial': historial
    })
