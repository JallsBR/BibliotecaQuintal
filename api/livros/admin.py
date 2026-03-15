from django.contrib import admin
from .models import *

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at', 'updated_at')
    search_fields = ('nome',)
    ordering = ('nome',)

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at', 'updated_at')
    search_fields = ('nome',)
    ordering = ('nome',)    

@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at', 'updated_at')
    search_fields = ('nome',)
    ordering = ('nome',)    

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'get_autores', 'editora', 'get_categorias', 'created_at', 'updated_at')
    search_fields = ('titulo', 'autores__nome', 'editora__nome', 'categorias__nome')
    ordering = ('titulo',)

    def get_autores(self, obj):
        return ", ".join(obj.autores.values_list('nome', flat=True))

    get_autores.short_description = 'Autores'

    def get_categorias(self, obj):
        return ", ".join(obj.categorias.values_list('nome', flat=True))

    get_categorias.short_description = 'Categorias'


