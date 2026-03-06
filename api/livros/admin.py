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
    list_display = ('titulo', 'autor', 'editora', 'categoria', 'created_at', 'updated_at')
    search_fields = ('titulo', 'autor', 'editora', 'categoria')
    ordering = ('titulo',)    


