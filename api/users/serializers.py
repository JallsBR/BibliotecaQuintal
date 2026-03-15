from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'last_name',
            'email',
            'is_superuser',
        )


class UserAdminSerializer(serializers.ModelSerializer):
    """Serializer para listagem/edição de usuários na configuração (superuser)."""
    groups_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'last_name',
            'email',
            'is_staff',
            'is_superuser',
            'groups',
            'groups_detail',
        )

    def get_groups_detail(self, obj):
        return [{'id': g.id, 'name': g.name} for g in obj.groups.all()]