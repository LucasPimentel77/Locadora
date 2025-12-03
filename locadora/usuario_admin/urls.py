from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('calendario/', views.calendario_reservas, name='calendario_reservas'),
    path('reservas/', views.gerenciar_reservas, name='gerenciar_reservas'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)