from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="lista"),
    path("posts/nuevo/", views.PostCreateView.as_view(), name="crear"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="detalle"),
    path("posts/<int:pk>/editar/", views.PostUpdateView.as_view(), name="editar"),
    path("posts/<int:pk>/eliminar/", views.PostDeleteView.as_view(), name="eliminar"),
]
