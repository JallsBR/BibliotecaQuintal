from rest_framework import serializers
from .models import *


class LeitorRecompensaSerializer(serializers.ModelSerializer):
    recompensa_nome = serializers.CharField(source='recompensa.nome', read_only=True)
    recompensa_descricao = serializers.CharField(source='recompensa.descricao', read_only=True)
    recompensa_pontuacao = serializers.IntegerField(source='recompensa.pontuacao', read_only=True)

    class Meta:
        model = LeitorRecompensa
        fields = ['id', 'leitor', 'recompensa', 'data_resgate', 'recompensa_nome', 'recompensa_descricao', 'recompensa_pontuacao']
        read_only_fields = []

    def validate(self, attrs):
        if not self.instance and attrs.get('leitor') and attrs.get('recompensa'):
            pontuacao_nec = attrs['recompensa'].pontuacao
            pontuacao_disp = attrs['leitor'].pontuacao_atual
            if pontuacao_disp < pontuacao_nec:
                raise serializers.ValidationError(
                    {'recompensa': f'Pontuação insuficiente. Necessário: {pontuacao_nec}, disponível: {pontuacao_disp}.'}
                )
        return attrs


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
        # Recompensas como lista de resgates (id, recompensa, data_resgate, etc.)
        resgates = []
        for lr in instance.leitorrecompensa_set.all().select_related('recompensa'):
            resgates.append({
                'id': lr.id,
                'recompensa': lr.recompensa_id,
                'recompensa_nome': lr.recompensa.nome,
                'recompensa_descricao': lr.recompensa.descricao,
                'recompensa_pontuacao': lr.recompensa.pontuacao,
                'data_resgate': lr.data_resgate,
            })
        data['recompensas_resgatadas'] = resgates
        return data 

class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['leitor_nome'] = instance.leitor.nome if instance.leitor_id else ''
        data['livro_titulo'] = instance.livro.titulo if instance.livro_id else ''
        return data

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['leitor_nome'] = instance.leitor.nome if instance.leitor_id else ''
        data['livro_titulo'] = instance.livro.titulo if instance.livro_id else ''
        return data
            