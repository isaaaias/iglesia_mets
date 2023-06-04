# Generated by Django 4.0.2 on 2023-05-27 00:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Versiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libro', models.CharField(max_length=100)),
                ('capitulo', models.IntegerField()),
                ('versiculo', models.IntegerField()),
                ('texto', models.TextField()),
                ('pagina', models.TextField()),
                ('posicion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion_corta', models.TextField()),
                ('contenido', models.TextField()),
                ('fecha_evento', models.DateField()),
                ('hora_evento', models.TimeField()),
                ('direccion', models.CharField(max_length=200)),
                ('imagen_evento', models.ImageField(blank=True, null=True, upload_to='eventos/')),
                ('id_encargado', models.CharField(max_length=200)),
                ('fecha_publicacion', models.DateField(auto_now_add=True)),
                ('hora_publicacion', models.TimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
