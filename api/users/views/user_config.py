from rest_framework import generics
from users.models import User
from users.serializers import UserAdminSerializer
from users.permissions import IsSuperuser


class UserListView(generics.ListAPIView):
    """Lista todos os usuários (somente superuser)."""
    serializer_class = UserAdminSerializer
    permission_classes = [IsSuperuser]
    queryset = User.objects.all().order_by('username')


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Consulta e atualiza um usuário (grupos, is_staff, two_factor_enabled) — somente superuser."""
    serializer_class = UserAdminSerializer
    permission_classes = [IsSuperuser]
    queryset = User.objects.all()
