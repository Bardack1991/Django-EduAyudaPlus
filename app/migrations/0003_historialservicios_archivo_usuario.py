# Generated by Django 5.0.3 on 2024-04-13 23:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_servicio_tipoayuda_archivosusuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialservicios',
            name='archivo_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.archivosusuario'),
            preserve_default=False,
        ),
    ]