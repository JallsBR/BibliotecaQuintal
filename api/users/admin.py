from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'email', 'two_factor_enabled')
    list_filter = ('two_factor_enabled', 'is_staff', 'is_superuser')
    search_fields = ('username', 'last_name', 'email')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        obj.save()