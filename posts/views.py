from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    """Portada: muestra los posts publicados.
    Con ?q= busca por título o contenido y con ?tag= filtra por tag."""

    model = Post
    template_name = "posts/lista.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        posts = Post.objects.filter(estado=Post.Estado.PUBLICADO)
        busqueda = self.request.GET.get("q", "").strip()
        tag = self.request.GET.get("tag", "").strip()
        if busqueda:
            posts = posts.filter(Q(titulo__icontains=busqueda) | Q(contenido__icontains=busqueda))
        if tag:
            posts = posts.filter(tags__icontains=tag)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["busqueda"] = self.request.GET.get("q", "").strip()
        context["tag"] = self.request.GET.get("tag", "").strip()
        return context


class PostDetailView(DetailView):
    """Detalle de un post. Los borradores y archivados solo los ve su autor."""

    model = Post
    template_name = "posts/detalle.html"

    def get_queryset(self):
        publicados = Q(estado=Post.Estado.PUBLICADO)
        if self.request.user.is_authenticated:
            return Post.objects.filter(publicados | Q(autor=self.request.user))
        return Post.objects.filter(publicados)


# Las tres views siguientes usan LoginRequiredMixin: si el usuario no inició
# sesión, Django lo redirige al login antes de ejecutar la view.


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/formulario.html"
    extra_context = {"titulo_pagina": "Nuevo post"}

    def form_valid(self, form):
        form.instance.autor = self.request.user  # el autor es quien está logueado
        messages.success(self.request, "Post creado correctamente.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/formulario.html"
    extra_context = {"titulo_pagina": "Editar post"}

    def get_queryset(self):
        # Solo se pueden editar los posts propios (si no, da 404)
        return Post.objects.filter(autor=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Post actualizado correctamente.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/confirmar_eliminar.html"
    success_url = reverse_lazy("posts:lista")

    def get_queryset(self):
        # Solo se pueden eliminar los posts propios (si no, da 404)
        return Post.objects.filter(autor=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Post eliminado.")
        return super().form_valid(form)
