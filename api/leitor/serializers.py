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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['pontuacao_atual'] = instance.pontuacao_atual
        return data 

class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        instance = self.instance if self.instance else Emprestimo()
        for key, value in attrs.items():
            setattr(instance, key, value)
        instance.clean()
        return attrs

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
            