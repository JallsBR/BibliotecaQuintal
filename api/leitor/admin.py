from django.contrib import admin
from .models import Recompensa, Leitor, Emprestimo, Reserva


@admin.register(Recompensa)
class RecompensaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pontuacao', 'created_at', 'updated_at')
    search_fields = ('nome',)
    ordering = ('pontuacao', 'nome')


@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pontuacao_atual', 'created_at', 'updated_at')
    search_fields = ('nome',)
    ordering = ('pontuacao_atual', 'nome')


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('leitor', 'livro', 'data_emprestimo', 'data_devolucao', 'created_at', 'updated_at')
    search_fields = ('leitor', 'livro')
    ordering = ('data_emprestimo', 'leitor', 'livro')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('leitor', 'livro', 'data_reserva', 'data_expiracao', 'created_at', 'updated_at')
    search_fields = ('leitor', 'livro')
    ordering = ('data_reserva', 'leitor', 'livro')
