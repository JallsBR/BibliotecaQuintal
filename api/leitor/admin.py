from django.contrib import admin
from .models import Recompensa, Leitor, Emprestimo, Reserva


@admin.register(Recompensa)
class RecompensaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pontuacao', 'ativo', 'created_at', 'updated_at')
    list_filter = ('ativo',)
    search_fields = ('nome', 'descricao')
    ordering = ('pontuacao', 'nome')


@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'pontuacao_atual', 'pontuacao_total', 'ativo', 'created_at')
    list_filter = ('ativo',)
    search_fields = ('nome', 'email', 'telefone', 'cpf')
    ordering = ('nome',)


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('leitor', 'livro', 'data_emprestimo', 'data_devolucao', 'devolvido', 'created_at')
    list_filter = ('devolvido',)
    search_fields = ('leitor__nome', 'livro__titulo')
    ordering = ('-data_emprestimo',)
    raw_id_fields = ('leitor', 'livro')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('leitor', 'livro', 'data_reserva', 'data_expiracao', 'ativo', 'created_at')
    list_filter = ('ativo',)
    search_fields = ('leitor__nome', 'livro__titulo')
    ordering = ('-data_reserva',)
    raw_id_fields = ('leitor', 'livro')
