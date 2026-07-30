from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

from app.views import DashboardStatsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/livros/', include('livros.urls')),
    path('api/v1/leitor/', include('leitor.urls')),
    path('api/v1/dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    # Produção: o host Nginx proxia /media/ → API (8082). static() só ativa com DEBUG.
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
