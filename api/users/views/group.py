from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

from users.serializers_group import GroupSerializer
from users.permissions import IsSuperuser


class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        return Group.objects.all().order_by('name')


class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        return Group.objects.all()

    def get_object(self):
        return get_object_or_404(Group, pk=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'detail': 'Grupo removido com sucesso.'},
            status=status.HTTP_200_OK,
        )
