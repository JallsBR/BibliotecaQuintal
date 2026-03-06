from django.urls import path
from . import views


urlpatterns = [
    # Recompensas
    path("recompensas/", views.RecompensaListCreateView.as_view(), name="recompensa-list-create"),
    path("recompensas/<int:pk>/", views.RecompensaRetrieveUpdateDestroyView.as_view(), name="recompensa-retrieve-update-destroy"),

    # Leitores
    path("leitores/", views.LeitorListCreateView.as_view(), name="leitor-list-create"),
    path("leitores/<int:pk>/", views.LeitorRetrieveUpdateDestroyView.as_view(), name="leitor-retrieve-update-destroy"),

    # Empréstimos
    path("emprestimos/", views.EmprestimoListCreateView.as_view(), name="emprestimo-list-create"),
    path("emprestimos/<int:pk>/", views.EmprestimoRetrieveUpdateDestroyView.as_view(), name="emprestimo-retrieve-update-destroy"),

    # Reservas
    path("reservas/", views.ReservaListCreateView.as_view(), name="reserva-list-create"),
    path("reservas/<int:pk>/", views.ReservaRetrieveUpdateDestroyView.as_view(), name="reserva-retrieve-update-destroy"),
]
