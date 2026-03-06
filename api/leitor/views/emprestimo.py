from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from ..models import Emprestimo
from ..serializers import EmprestimoSerializer


class EmprestimoListCreateView(generics.ListCreateAPIView):
    serializer_class = EmprestimoSerializer
    permission_classes = [IsAuthenticated]

    # Filtros e ordenação
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "leitor": ["exact"],
        "livro": ["exact"],
        "ativo": ["exact"],
        "data_emprestimo": ["exact", "gte", "lte"],
    }
    ordering_fields = ["data_emprestimo", "data_devolucao", "created_at"]
    ordering = ["-data_emprestimo"]

    def get_queryset(self):
        return Emprestimo.objects.all()


class EmprestimoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmprestimoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Emprestimo.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"detail": "Empréstimo removido com sucesso."},
            status=status.HTTP_200_OK,
        )
