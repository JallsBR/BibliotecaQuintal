from rest_framework.generics import ListAPIView
from django.contrib.auth.models import Permission

from users.serializers_group import PermissionSerializer
from users.permissions import IsSuperuser


class PermissionListView(ListAPIView):
    serializer_class = PermissionSerializer
    permission_classes = [IsSuperuser]
    pagination_class = None  # retorna todas as permissões para uso no formulário de grupos

    def get_queryset(self):
        return Permission.objects.select_related('content_type').all().order_by('content_type__app_label', 'content_type__model', 'codename')
