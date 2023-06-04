"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from app import views
from django.conf import settings
from django.conf.urls.static import static
from app.views import listar_usuarios, crear_usuario, eliminar_cargo, crear_cargo, actualizar_cargo, listar_cargos, listar_versiculos, ver_usuario, actualizar_usuario, quienes_somos, mision
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('usuarios/<int:usuario_id>/editar/', actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('usuarios/<int:usuario_id>/', ver_usuario, name='ver_usuario'),
    path('listar_eventos/', views.listar_eventos, name='listar_eventos'),
    path('listar_eventos_publico/', views.ListarEventoPublicoView.as_view(), name='listar_eventos_publico'),
    path('eventos/modificar/<int:evento_id>/', views.modificar_evento, name='modificar_evento'),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('evento/<int:evento_id>/', views.ver_evento, name='ver_evento'),
    path('versiculos/', views.listar_versiculos, name='listar_versiculos'),
    path('versiculos/modificar/<int:versiculo_id>/', views.modificar_versiculo, name='modificar_versiculo'),
    path('login/', views.login_view, name='login'),
    path('quienes_somos/', quienes_somos, name='quienes_somos'),
    path('mision/', mision, name='mision'),
    path('galeria_nueva/', views.galeria_nueva, name='galeria_nueva'),
    path('albumes/', views.listar_albumes, name='listar_albumes'),
    path('galeria/<int:album_id>/', views.galeria, name='galeria'),
    path('crear_album/', views.crear_album  , name='crear_album'),
    # URL para el cierre de sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    # URL para la vista de perfil
    path('profile/', views.profile_view, name='profile'),
    path('crear_cargo/', crear_cargo, name='crear_cargo'),
    path('cargos/', listar_cargos, name='listar_cargos'),
    path('cargos/<int:cargo_id>/editar/', actualizar_cargo, name='actualizar_cargo'),
    path('cargos/<int:cargo_id>/eliminar/', eliminar_cargo, name='eliminar_cargo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)