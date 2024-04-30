from rest_framework import serializers
from .models import Servicio, HistorialServicios

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class HistorialServiciosSerializer(serializers.ModelSerializer):
    servicio = ServicioSerializer()

    class Meta:
        model = HistorialServicios
        fields = '__all__'