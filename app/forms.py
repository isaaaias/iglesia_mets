from django import forms
from .models import Evento
from .models import Usuario, Versiculo, Cargo, Galeria, Album
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'cargos', 'imagen', 'puede_gestionar_eventos', 'puede_gestionar_galerias', 'puede_gestionar_usuarios', 'puede_gestionar_cargos', 'puede_gestionar_versiculos']
        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomLoginForm(AuthenticationForm):
    # Agregar campos adicionales si es necesario
    # campo_personalizado = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




class VersiculoForm(forms.ModelForm):
    class Meta:
        model = Versiculo
        fields = ['libro', 'capitulo', 'versiculo', 'texto']
        
class ModificarVersiculoForm(forms.ModelForm):
    class Meta:
        model = Versiculo
        fields = ['texto']

class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"  # Asegúrate de cambiar esto a tus campos de nombre real

class EventoForm(forms.ModelForm):
    
    encargado = UserChoiceField(queryset=Usuario.objects.all())

    class Meta:
        model = Evento
        fields = ('titulo', 'descripcion_corta', 'contenido', 'fecha_evento', 'hora_evento', 'direccion', 'imagen_evento', 'encargado')
        exclude = ['fecha_publicacion', 'hora_publicacion']
        widgets = {
            'fecha_evento': forms.DateInput(attrs={'class': 'datepicker'}),
            'hora_evento': forms.TimeInput(attrs={'class': 'timepicker'}),
        }
        

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre']


def crear_cargo(request):
    # Obtener el usuario actual
    usuario_actual = request.user

    # Verificar si el usuario tiene el cargo requerido
    if not usuario_actual.cargos.filter(nombre='CargoEspecifico').exists():
        return redirect('perfil')  # Redirigir a la página de perfil si no tiene el cargo requerido

    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_cargos')
    else:
        form = CargoForm()
    
    context = {'form': form}
    return render(request, 'crear_cargo.html', context)


# Vista de actualización de cargo
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


class GaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria
        fields = ('titulo', 'imagen', 'descripcion', 'album')

class AlbumForm(forms.ModelForm):
    is_featured = forms.BooleanField(label='Destacado en index')
    class Meta:
        model = Album
        fields = ['nombre', 'imagen', 'is_featured']