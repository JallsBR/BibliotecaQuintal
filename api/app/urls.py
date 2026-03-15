from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app.views import DashboardStatsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/livros/', include('livros.urls')),
    path('api/v1/leitor/', include('leitor.urls')),
    path('api/v1/dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
