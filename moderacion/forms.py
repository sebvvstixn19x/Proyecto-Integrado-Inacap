from django import forms
from .models import Reporte, AccionModeracion


# -----------------------------
# Formulario para que los usuarios reporten contenido
# -----------------------------
class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['motivo']
        widgets = {
            'motivo': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'motivo': 'Motivo del reporte',
        }


# -----------------------------
# Formulario para que el admin decida qué hacer con un reporte
# -----------------------------
class AccionModeracionForm(forms.ModelForm):
    class Meta:
        model = AccionModeracion
        fields = ['accion']
        widgets = {
            'accion': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'accion': 'Acción a realizar',
        }
