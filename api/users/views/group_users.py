from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from users.models import User
from users.permissions import IsSuperuser


class GroupUsersView(APIView):
    """Lista e define os usuários de um grupo (somente superuser)."""
    permission_classes = [IsSuperuser]

    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        user_ids = list(group.user_set.values_list('id', flat=True))
        return Response({'user_ids': user_ids})

    def put(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        user_ids = request.data.get('user_ids')
        if not isinstance(user_ids, list):
            return Response(
                {'detail': 'Envie user_ids como lista de IDs.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        users = User.objects.filter(id__in=user_ids)
        group.user_set.set(users)
        return Response({'user_ids': list(users.values_list('id', flat=True))})
