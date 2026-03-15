"""
View de dashboard: retorna contagens agregadas para a home.
Apenas usuário autenticado; resposta mínima em JSON (números), sem dados sensíveis.
"""
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class DashboardStatsView(APIView):
    """
    GET: retorna um JSON com contagens para o dashboard da home.
    Qualquer usuário autenticado pode acessar; o retorno não transmite informações sensíveis.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from livros.models import Livro
        from leitor.models import Leitor, Emprestimo, Reserva, Recompensa

        hoje = timezone.localdate()
        payload = {
            'livros': Livro.objects.filter(ativo=True).count(),
            'leitores': Leitor.objects.filter(ativo=True).count(),
            'emprestimos_abertos': Emprestimo.objects.filter(
                devolvido=False, ativo=True
            ).count(),
            'emprestimos_em_atraso': Emprestimo.objects.filter(
                devolvido=False, ativo=True, data_devolucao__lt=hoje
            ).count(),
            'reservas_ativas': Reserva.objects.filter(
                ativo=True,
                data_expiracao__gte=hoje,
            ).count(),
            'recompensas': Recompensa.objects.filter(ativo=True).count(),
        }
        return Response(payload)
