"""
URL configuration for locadora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views, views_auth, views_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path('cadastro/', views_auth.cadastro, name='cadastro'),
    path('login/', views_auth.login_usuario, name='login'),
    path('logout/', views_auth.logout_usuario, name='logout'),
    path('perfil/', views_auth.perfil, name='perfil'),
    path('perfil/editar/', views_auth.editar_perfil, name='editar_perfil'),
    path("alugar/", views.alugar, name="alugar"),
    path("categorias/", include("categoria.urls")),
    path("reserva/", include("reserva.urls")),
    path('api/reservas/<int:reserva_id>/atualizar-status/', views_api.atualizar_status_reserva, name='atualizar_status_reserva'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
