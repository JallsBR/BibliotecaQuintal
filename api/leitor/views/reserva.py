from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from ..models import Reserva
from ..serializers import ReservaSerializer


class ReservaListCreateView(generics.ListCreateAPIView):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    # Filtros e ordenação
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "leitor": ["exact"],
        "livro": ["exact"],
        "ativo": ["exact"],
        "data_reserva": ["exact", "gte", "lte"],
    }
    ordering_fields = ["data_reserva", "data_expiracao", "created_at"]
    ordering = ["-data_reserva"]

    def get_queryset(self):
        return Reserva.objects.all()


class ReservaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reserva.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"detail": "Reserva removida com sucesso."},
            status=status.HTTP_200_OK,
        )
