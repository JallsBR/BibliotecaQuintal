from rest_framework import serializers
from .models import *

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class EditoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editora
        fields = '__all__'  
        read_only_fields = ['created_at', 'updated_at']

class LivroSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.nome', read_only=True)
    editora_nome = serializers.CharField(source='editora.nome', read_only=True)
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    qtd_disponivel = serializers.IntegerField(read_only=True)

    class Meta:
        model = Livro
        fields = '__all__'
        read_only_fields = [
            'created_at', 'updated_at',
            'qtd_emprestados',  # controlado pelo signal de empréstimo/devolução
            'qtd_disponivel',  # calculado: qtd_total - qtd_emprestados
            'is_disponivel',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['qtd_disponivel'] = instance.qtd_disponivel
        return data

