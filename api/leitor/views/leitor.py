from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from ..models import Leitor
from ..serializers import LeitorSerializer


class LeitorListCreateView(generics.ListCreateAPIView):
    serializer_class = LeitorSerializer
    permission_classes = [IsAuthenticated]

    # Filtros e ordenação
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "nome": ["exact", "icontains"],
        "email": ["exact", "icontains"],
        "ativo": ["exact"],
        "cidade": ["exact", "icontains"],
    }
    ordering_fields = ["nome", "email", "pontuacao_atual", "created_at"]
    ordering = ["nome"]

    def get_queryset(self):
        return Leitor.objects.all()


class LeitorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeitorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Leitor.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"detail": "Leitor removido com sucesso."},
            status=status.HTTP_200_OK,
        )
