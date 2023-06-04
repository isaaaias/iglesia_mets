from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Usuario, Cargo, Galeria, Album
from .forms import UsuarioForm, CargoForm, CustomLoginForm, GaleriaForm, AlbumForm
from django.shortcuts import render
from app.models import Evento, Usuario, Versiculo
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .forms import UsuarioForm, EventoForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
import locale
from django.utils.decorators import method_decorator
from datetime import date
from calendar import monthrange
import calendar
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.

def tiene_permisos_gestionar_eventos(user):
    return user.puede_gestionar_eventos

def tiene_permisos_gestionar_galerias(user):
    return user.puede_gestionar_galerias

def tiene_permisos_gestionar_usuarios(user):
    return user.puede_gestionar_usuarios

def tiene_permisos_gestionar_cargos(user):
    return user.puede_gestionar_cargos

def tiene_permisos_gestionar_versiculos(user):
    return user.puede_gestionar_versiculos


def quienes_somos(request):
    return render(request, 'html/quienes_somos.html')

def mision(request):
    return render(request, 'html/mision.html')

def galeria(request):
    return render(request, 'html/galeria.html')


class ListarEventoPublicoView(ListView):
    model = Evento
    template_name = 'html/listar_eventos_publico.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        year = today.year

        meses_restantes = range(today.month, 13)  # Obtener los meses restantes del año

        eventos_meses = {}  # Diccionario para almacenar los eventos de cada mes

        # Establecer la configuración regional en español
        locale.setlocale(locale.LC_TIME, 'es_ES')

        for month in meses_restantes:
            _, num_days = monthrange(year, month)
            dias_mes = [{'numero': dia, 'evento': []} for dia in range(1, num_days + 1)]

            eventos = self.get_queryset()
            for evento in eventos:
                if evento.fecha_evento.year == year and evento.fecha_evento.month == month:
                    dia = evento.fecha_evento.day
                    dias_mes[dia - 1]['evento'].append(evento)

            nombre_mes = calendar.month_name[month]  # Obtener el nombre del mes en inglés
            nombre_mes_es = calendar.month_name[month].capitalize()  # Traducir el nombre del mes al español
            eventos_meses[nombre_mes_es] = dias_mes

        context['eventos_meses'] = eventos_meses.items()  # Pasar el diccionario al contexto
        return context




class IndexView(ListView):
    model = Evento
    template_name = 'html/index.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        now = timezone.now()
        eventos = Evento.objects.filter(fecha_evento__gte=now.date()).exclude(fecha_evento=now.date(), hora_evento__lt=now.time()).order_by('fecha_evento', 'hora_evento')[:6]
        return eventos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Establecer el locale en español
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        # Convertir las fechas de eventos al formato español
        for evento in context['eventos']:
            fecha_evento = evento.fecha_evento.strftime('%d de %B de %Y')
            evento.fecha_evento = fecha_evento.capitalize()
        # Obtener las primeras 4 galerías
        primeras_galerias = Galeria.objects.filter(album__is_featured=True).order_by('id')[:6]
        context['galerias'] = primeras_galerias
        context['versiculos'] = Versiculo.objects.all()
        return context

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_usuarios, login_url='profile')
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'html/listar_usuarios.html', {'usuarios': usuarios})

def ver_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    usuario_encargado = get_object_or_404(Usuario, pk=evento.id_encargado)
    return render(request, 'html/evento.html', {'evento': evento, 'usuario_encargado': usuario_encargado})

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_usuarios, login_url='profile')
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect('listar_usuarios')

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_usuarios, login_url='profile')
def actualizar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('ver_usuario', usuario_id=usuario_id)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'actualizar_usuario.html', {'form': form, 'usuario': usuario})

def ver_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'ver_usuario.html', {'usuario': usuario})


@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_usuarios, login_url='profile')
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.password = make_password(password)  # Hashear la contraseña
            user.save()

            # Obtener los cargos seleccionados en el formulario
            cargos_ids = form.cleaned_data['cargos']
            cargos = Cargo.objects.filter(id__in=cargos_ids)

            # Asignar los cargos al usuario
            user.cargos.set(cargos)

            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    
    context = {'form': form}
    return render(request, 'html/crear_usuario.html', context)

# def vista_admin(request):
#     usuario = request.user

#     if usuario.cargos.filter(nombre='Admin').exists() or usuario.is_superuser:
#         # Lógica para mostrar los reportes o usuarios registrados
#         return render(request, 'listar_.html')
#     else:
#         # Lógica para mostrar un mensaje de error o redirigir a otra página
#         return render(request, 'sin_permisos.html')
@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_eventos, login_url='profile')
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            autor_id = request.user.id
            autor = get_object_or_404(Usuario, id=autor_id)
            evento.autor = autor
            encargado_id = request.POST.get('encargado')
            evento.id_encargado = str(encargado_id)  # convertir el id del encargado en una cadena
            evento.save()
            return redirect('listar_eventos')
        else:
            print(form.errors)
    else:
        form = EventoForm()

    return render(request, 'html/crear_evento.html', {'form': form, 'errors': form.errors})

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_eventos, login_url='profile')
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    evento.delete()
    return redirect('listar_eventos')

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_eventos, login_url='profile')
def modificar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.POST.get('titulo')
        descripcion_corta = request.POST.get('descripcion_corta')
        contenido = request.POST.get('contenido')
        fecha_evento = request.POST.get('fecha_evento')
        hora_evento = request.POST.get('hora_evento')
        
        # Actualizar los campos del evento
        evento.titulo = titulo
        evento.descripcion_corta = descripcion_corta
        evento.contenido = contenido
        evento.fecha_evento = fecha_evento
        evento.hora_evento = hora_evento
        evento.save()
        
        return redirect('listar_eventos')
    
    return render(request, 'html/modificar_evento.html', {'evento': evento})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Resto de la lógica de inicio de sesión
                # Guardar datos del usuario en la sesión
                request.session['datos_usuario'] = {
                'username': user.username,
                # Agrega más datos que desees almacenar en la sesión
            }
                return redirect('profile')
            else:
                form.add_error(None, 'Credenciales inválidas')
    else:
        form = CustomLoginForm(request)
    return render(request, 'html/login.html', {'form': form})


@login_required(login_url='login')
def profile_view(request):
    usuario = request.user
    cargos = usuario.cargos.all()
    context = {'cargos': cargos}

    if usuario.puede_gestionar_eventos:
        context['mostrar_eventos'] = True
    if usuario.puede_gestionar_galerias:
        context['mostrar_galerias'] = True
    if usuario.puede_gestionar_usuarios:
        context['mostrar_usuarios'] = True
    if usuario.puede_gestionar_cargos:
        context['mostrar_cargos'] = True
    if usuario.puede_gestionar_versiculos:
        context['mostrar_versiculos'] = True
    return render(request, 'html/perfil.html', context)


# @method_decorator(login_required(login_url='login'), name='dispatch')
# class ListarEventoView(UserPassesTestMixin, ListView):
#     model = Evento
#     template_name = 'html/listar_eventos.html'
#     context_object_name = 'eventos'

#     def test_func(self):
#         return self.request.user.puede_gestionar_eventos

#     def get_login_url(self):
#         return 'login'
@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_eventos, login_url='profile')
def listar_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'html/listar_eventos.html', {'eventos': eventos})

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_versiculos, login_url='profile')
def listar_versiculos(request):
    versiculos = Versiculo.objects.all()
    return render(request, 'html/versiculos.html', {'versiculos': versiculos})

def listar_versiculos_pagina(request):
    versiculos = Versiculo.objects.order_by('pagina')
    return render(request, 'versiculos.html', {'versiculos': versiculos})

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_versiculos, login_url='profile')
def modificar_versiculo(request, versiculo_id):
    versiculo = Versiculo.objects.get(id=versiculo_id)

    if request.method == 'POST':
        versiculo.libro = request.POST.get('libro')
        versiculo.capitulo = request.POST.get('capitulo')
        versiculo.versiculo = request.POST.get('versiculo')
        versiculo.texto = request.POST.get('texto')
        versiculo.save()
        return redirect('listar_versiculos')

    return render(request, 'html/modificar_versiculo.html', {'versiculo': versiculo})



@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_cargos, login_url='profile')
def crear_cargo(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_cargos')
    else:
        form = CargoForm()
    
    context = {'form': form}
    return render(request, 'html/crear_cargo.html', context)

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_cargos, login_url='profile')
def listar_cargos(request):
    cargos = Cargo.objects.all()
    return render(request, 'html/listar_cargos.html', {'cargos': cargos})

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_cargos, login_url='profile')
def actualizar_cargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('listar_cargos')
    else:
        form = CargoForm(instance=cargo)
    
    context = {'form': form, 'cargo': cargo}
    return render(request, 'actualizar_cargo.html', context)

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_cargos, login_url='profile')
def eliminar_cargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id)
    cargo.delete()
    return redirect('listar_cargos')


def galeria(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    galerias = Galeria.objects.filter(album=album)
    return render(request, 'html/galeria.html', {'album': album, 'galerias': galerias})


@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_galerias, login_url='profile')
def galeria_nueva(request):
    if request.method == 'POST':
        form = GaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            galeria = form.save()
            return redirect('/', pk=galeria.pk)
    else:
        form = GaleriaForm()
    albums = Album.objects.all()
    return render(request, 'html/agregar_imagen.html', {'form': form, 'albums': albums})

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_galerias, login_url='profile')
def galeria_editar(request, pk):
    galeria = get_object_or_404(Galeria, pk=pk)
    if request.method == 'POST':
        form = GaleriaForm(request.POST, request.FILES, instance=galeria)
        if form.is_valid():
            galeria = form.save()
            return redirect('galeria_detalle', pk=galeria.pk)
    else:
        form = GaleriaForm(instance=galeria)
    return render(request, 'galeria/galeria_editar.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_galerias, login_url='profile')
def galeria_eliminar(request, pk):
    galeria = get_object_or_404(Galeria, pk=pk)
    galeria.delete()
    return redirect('galeria_lista')


def listar_albumes(request):
    albumes = Album.objects.all()
    return render(request, 'html/albumes.html', {'albumes': albumes})

@login_required(login_url='login')
@user_passes_test(tiene_permisos_gestionar_galerias, login_url='profile')
def crear_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('html/galeria.html')
    else:
        form = AlbumForm()
    return render(request, 'html/crear_album.html', {'form': form})