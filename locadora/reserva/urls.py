from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    
    path('escolher-grupo/<slug:slug_grupo>/', views.escolher_grupo, name='escolher_grupo'),
    path('finalizar-reserva/<slug:slug_grupo>/', views.finalizar_reserva, name='finalizar_reserva'),
    path("<int:reserva_id>/", views.detalhes_reserva, name="detalhes_reserva"),
    path("api/verificar-cupom/", views.verificar_cupom, name="verificar_cupom"),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('minhas-reservas/<int:reserva_id>/', views.detalhes_minha_reserva, name='detalhes_minha_reserva'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)