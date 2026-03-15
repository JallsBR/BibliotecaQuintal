from rest_framework import serializers
from django.contrib.auth.models import Group, Permission


class PermissionSerializer(serializers.ModelSerializer):
    content_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type', 'content_type_name']

    def get_content_type_name(self, obj):
        return str(obj.content_type) if obj.content_type else ''


class GroupSerializer(serializers.ModelSerializer):
    permissions_detail = PermissionSerializer(source='permissions', many=True, read_only=True)
    user_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permissions_detail', 'user_count']

    def get_user_count(self, obj):
        return obj.user_set.count()
