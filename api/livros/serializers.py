from rest_framework import serializers
from .models import Categoria, Autor, Editora, Livro

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
    autores = serializers.PrimaryKeyRelatedField(
        queryset=Autor.objects.all(),
        many=True,
        required=False,
        allow_empty=True,
    )
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        many=True,
        required=False,
        allow_empty=True,
    )
    autores_nomes = serializers.SerializerMethodField(read_only=True)
    categorias_nomes = serializers.SerializerMethodField(read_only=True)
    editora_nome = serializers.CharField(source='editora.nome', read_only=True)
    qtd_disponivel = serializers.IntegerField(read_only=True)

    class Meta:
        model = Livro
        fields = '__all__'
        read_only_fields = [
            'created_at',
            'updated_at',
            'qtd_emprestados',  # controlado pelo signal de empréstimo/devolução
            'qtd_disponivel',  # calculado: qtd_total - qtd_emprestados
            'is_disponivel',
        ]

    def get_autores_nomes(self, obj):
        return list(obj.autores.values_list('nome', flat=True))

    def get_categorias_nomes(self, obj):
        return list(obj.categorias.values_list('nome', flat=True))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['qtd_disponivel'] = instance.qtd_disponivel
        return data

