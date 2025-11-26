from django.urls import path
from . import views

urlpatterns = [
    path('reportar/reseña/<int:reseña_id>/', views.reportar_reseña, name='reportar_reseña'),
    path('reportar/comentario/<int:comentario_id>/', views.reportar_comentario, name='reportar_comentario'),
    path('panel/', views.panel_moderacion, name='panel_moderacion'),
    path('resolver/<int:reporte_id>/', views.resolver_reporte, name='resolver_reporte'),
]
