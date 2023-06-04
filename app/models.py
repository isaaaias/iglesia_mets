from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

# Create your models here.
class Cargo(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    cargos = models.ManyToManyField(Cargo)
    imagen = models.ImageField(upload_to='user_images/', blank=True, null=True)
    puede_gestionar_eventos = models.BooleanField(default=False)
    puede_gestionar_galerias = models.BooleanField(default=False)
    puede_gestionar_usuarios = models.BooleanField(default=False)
    puede_gestionar_cargos = models.BooleanField(default=False)
    puede_gestionar_versiculos = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion_corta = models.TextField()
    contenido = models.TextField()
    fecha_evento = models.DateField()
    hora_evento = models.TimeField()
    direccion = models.CharField(max_length=200)
    imagen_evento = models.ImageField(upload_to='eventos/', null=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_encargado = models.CharField(max_length=200)
    fecha_publicacion = models.DateField(auto_now_add=True)
    hora_publicacion = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Versiculo(models.Model):
    libro = models.CharField(max_length=100)
    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    texto = models.TextField()
    pagina = models.TextField()
    posicion = models.TextField()


    def __str__(self):
        return f"{self.libro} {self.capitulo}:{self.versiculo}"
    

    
class Album(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='albumes/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Galeria(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='galerias/')
    descripcion = models.TextField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.titulo