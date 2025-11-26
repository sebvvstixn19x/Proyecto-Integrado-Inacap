from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReporteForm, AccionModeracionForm
from .models import Reporte
from biblioteca.models import Reseña, Comentario


# -----------------------------
# Reportar reseña
# -----------------------------
@login_required
def reportar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.reseña = reseña
            reporte.save()
            messages.success(request, "Reporte enviado correctamente.")
            return redirect('detalle_libro', reseña.libro.id)
    else:
        form = ReporteForm()
    return render(request, 'moderacion/reportar.html', {'form': form, 'reseña': reseña})


# -----------------------------
# Reportar comentario
# -----------------------------
@login_required
def reportar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.comentario = comentario
            reporte.save()
            messages.success(request, "Reporte enviado correctamente.")
            return redirect('detalle_libro', comentario.reseña.libro.id)
    else:
        form = ReporteForm()
    return render(request, 'moderacion/reportar.html', {'form': form, 'comentario': comentario})


# -----------------------------
# Panel de moderación (solo admins)
# -----------------------------
@login_required
def panel_moderacion(request):
    if not request.user.is_admin:
        return redirect('homeGeneral')

    reportes_pendientes = Reporte.objects.filter(revisado=False).order_by('-fecha')
    reportes_resueltos = Reporte.objects.filter(revisado=True).order_by('-fecha')

    return render(request, 'moderacion/panel.html', {
        'reportes_pendientes': reportes_pendientes,
        'reportes_resueltos': reportes_resueltos
    })


# -----------------------------
# Resolver reporte (solo admins)
# -----------------------------
@login_required
def resolver_reporte(request, reporte_id):
    if not request.user.is_admin:
        return redirect('homeGeneral')

    reporte = get_object_or_404(Reporte, id=reporte_id)
    if request.method == 'POST':
        form = AccionModeracionForm(request.POST)
        if form.is_valid():
            accion = form.save(commit=False)
            accion.reporte = reporte
            accion.administrador = request.user
            accion.save()
            reporte.revisado = True
            reporte.save()
            messages.success(request, "Reporte marcado como resuelto.")
            return redirect('panel_moderacion')
    else:
        form = AccionModeracionForm()
    return render(request, 'moderacion/resolver.html', {
        'form': form,
        'reporte': reporte
    })
