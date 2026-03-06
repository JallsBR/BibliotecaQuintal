from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from ..models import Categoria
from ..serializers import CategoriaSerializer


class CategoriaListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

    # Filtros e ordenação
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "nome": ["exact", "icontains"],
    }
    ordering_fields = ["nome", "created_at"]
    ordering = ["nome"]

    def get_queryset(self):
        return Categoria.objects.all()


class CategoriaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Categoria.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"detail": "Categoria removida com sucesso."},
            status=status.HTTP_200_OK,
        )

