from rest_framework import serializers
from .models import *

class RecompensaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recompensa
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class LeitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leitor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at'] 

class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
            