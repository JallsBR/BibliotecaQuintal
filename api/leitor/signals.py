"""
Signals para Emprestimo:
- Ao criar: empresta o livro (livro.qtd_emprestados += 1). qtd_disponivel = qtd_total - qtd_emprestados (calculado).
- Ao devolver: devolve o livro (livro.qtd_emprestados -= 1) e credita pontuação ao leitor.
- Ao excluir: se o empréstimo ainda não estava devolvido (devolvido=False), devolve o livro (qtd_emprestados -= 1).
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Emprestimo
from livros.models import Livro


@receiver(post_save, sender=Emprestimo)
def atualizar_livro_ao_emprestar_ou_devolver(sender, instance, created, **kwargs):
    livro = instance.livro
    if not instance.livro_id:
        return

    if created:
        # Empréstimo novo: aumentar qtd_emprestados (qtd_disponivel = qtd_total - qtd_emprestados é calculado)
        livro.refresh_from_db()
        qtd_total = livro.qtd_total or 0
        qtd_emp = livro.qtd_emprestados or 0
        if (qtd_total - qtd_emp) < 1:
            return
        novo_emp = qtd_emp + 1
        Livro.objects.filter(pk=livro.pk).update(
            qtd_emprestados=novo_emp,
            is_disponivel=(qtd_total - novo_emp) > 0,
        )
        return

    # Devolução efetiva: só quando devolvido=True (e ainda não creditou pontuação)
    if not instance.devolvido or instance.pontuacao_creditada:
        return

    # Devolver o livro: diminuir qtd_emprestados
    livro.refresh_from_db()
    qtd_total = livro.qtd_total or 0
    qtd_emp = livro.qtd_emprestados or 0
    if qtd_emp >= 1:
        novo_emp = qtd_emp - 1
        Livro.objects.filter(pk=livro.pk).update(
            qtd_emprestados=novo_emp,
            is_disponivel=(qtd_total - novo_emp) > 0,
        )

    # Creditar pontuação ao leitor
    pontos = (instance.livro.pontuacao or 0) if instance.livro_id else 0
    if pontos > 0:
        leitor = instance.leitor
        if leitor:
            leitor.pontuacao_total = (leitor.pontuacao_total or 0) + pontos
            leitor.save()

    Emprestimo.objects.filter(pk=instance.pk).update(pontuacao_creditada=True)


@receiver(post_delete, sender=Emprestimo)
def devolver_livro_ao_excluir_emprestimo(sender, instance, **kwargs):
    """
    Ao excluir um empréstimo: se ainda não estava devolvido, devolve o livro
    (diminui qtd_emprestados) para que qtd_disponivel volte a aumentar.
    Se já estava devolvido, não altera o livro (já foi contabilizado na devolução).
    """
    if not instance.livro_id or instance.devolvido:
        return
    livro = instance.livro
    livro.refresh_from_db()
    qtd_total = livro.qtd_total or 0
    qtd_emp = livro.qtd_emprestados or 0
    if qtd_emp >= 1:
        novo_emp = qtd_emp - 1
        Livro.objects.filter(pk=livro.pk).update(
            qtd_emprestados=novo_emp,
            is_disponivel=(qtd_total - novo_emp) > 0,
        )
