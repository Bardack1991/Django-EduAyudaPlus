from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=20,  choices=settings.ROLES)

    def __str__(self):
        return self.user.username + ' - ' + self.role
    

class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre_servicio

class HistorialServicios(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_servicio = models.DateField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    archivo_usuario = models.ForeignKey('ArchivosUsuario', on_delete=models.CASCADE)  # Nueva línea

    def __str__(self):
        return f"{self.fecha_servicio} - {self.servicio.nombre_servicio}"

class ArchivosUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    url_archivo = models.URLField()
    nombre_archivo = models.CharField(max_length=255)
    tipo_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_archivo} ({self.fecha_subida})"

class MesaDeAyuda(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_ayuda = models.ForeignKey('TipoAyuda', on_delete=models.CASCADE)
    comentario = models.TextField()
    correo = models.EmailField()
    fecha_consulta = models.DateTimeField(auto_now_add=True)

class TipoAyuda(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_ayuda = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_ayuda

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=1))

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.username} Token"
        