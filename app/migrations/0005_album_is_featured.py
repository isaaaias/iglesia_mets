# Generated by Django 4.0.2 on 2023-05-27 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_album_galeria_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]