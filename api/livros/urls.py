from django.urls import path
from . import views


urlpatterns = [
    # Categorias
    path("categorias/", views.CategoriaListCreateView.as_view(), name="categoria-list-create"),    
    path("categorias/<int:pk>/", views.CategoriaRetrieveUpdateDestroyView.as_view(), name="categoria-retrieve-update-destroy"),
    
    # Autores
    path("autores/", views.AutorListCreateView.as_view(), name="autor-list-create"),
    path("autores/<int:pk>/", views.AutorRetrieveUpdateDestroyView.as_view(), name="autor-retrieve-update-destroy"),
    

    # Editoras
    path("editoras/", views.EditoraListCreateView.as_view(), name="editora-list-create"),
    path("editoras/<int:pk>/", views.EditoraRetrieveUpdateDestroyView.as_view(), name="editora-retrieve-update-destroy"),

    # Livros
    path("livros/", views.LivroListCreateView.as_view(), name="livro-list-create"),
    path("livros/<int:pk>/", views.LivroRetrieveUpdateDestroyView.as_view(), name="livro-retrieve-update-destroy"),
]

