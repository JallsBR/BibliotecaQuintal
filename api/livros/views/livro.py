from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from ..models import Livro
from ..serializers import LivroSerializer


class LivroListCreateView(generics.ListCreateAPIView):
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

    # Filtros e ordenação
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "titulo": ["exact", "icontains"],
        "ativo": ["exact"],
        "is_disponivel": ["exact"],
        "idioma": ["exact", "icontains"],
        "ano_publicacao": ["exact", "gte", "lte"],
        "autor": ["exact"],
        "editora": ["exact"],
        "categoria": ["exact"],
    }
    ordering_fields = [
        "titulo",
        "ano_publicacao",
        "qtd_disponivel",
        "created_at",
    ]
    ordering = ["titulo"]

    def get_queryset(self):
        return Livro.objects.all()


class LivroRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Livro.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"detail": "Livro removido com sucesso."},
            status=status.HTTP_200_OK,
        )

