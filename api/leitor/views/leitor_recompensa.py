from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from ..models import LeitorRecompensa
from ..serializers import LeitorRecompensaSerializer


class LeitorRecompensaListCreateView(generics.ListCreateAPIView):
    serializer_class = LeitorRecompensaSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "leitor": ["exact"],
        "recompensa": ["exact"],
        "data_resgate": ["exact", "gte", "lte"],
    }
    ordering_fields = ["data_resgate", "id"]
    ordering = ["-data_resgate"]

    def get_queryset(self):
        return LeitorRecompensa.objects.select_related("leitor", "recompensa").all()


class LeitorRecompensaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeitorRecompensaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LeitorRecompensa.objects.select_related("leitor", "recompensa").all()

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Resgate de recompensa removido com sucesso."},
            status=status.HTTP_200_OK,
        )
