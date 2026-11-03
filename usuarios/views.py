from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from posts.models import Post

from .forms import PerfilForm, RegistroForm, UsuarioForm
from .models import Perfil


def registro(request):
    """Crea la cuenta y deja al usuario con la sesión iniciada."""
    if request.user.is_authenticated:
        return redirect("posts:lista")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"¡Bienvenido/a, {usuario.username}! Tu cuenta fue creada.")
            return redirect("posts:lista")
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})


def perfil(request, username):
    """Perfil público de un usuario con sus posts publicados.
    Si es el propio perfil, también muestra borradores y archivados."""
    usuario = get_object_or_404(User, username=username)
    perfil_usuario, _ = Perfil.objects.get_or_create(usuario=usuario)
    posts = Post.objects.filter(autor=usuario)
    if request.user != usuario:
        posts = posts.filter(estado=Post.Estado.PUBLICADO)
    return render(
        request,
        "usuarios/perfil.html",
        {"usuario_perfil": usuario, "perfil": perfil_usuario, "posts": posts},
    )


@login_required
def mi_perfil(request):
    return redirect("usuarios:perfil", username=request.user.username)


@login_required
def editar_perfil(request):
    perfil_usuario, _ = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("usuarios:perfil", username=request.user.username)
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil_usuario)
    return render(
        request,
        "usuarios/editar_perfil.html",
        {"usuario_form": usuario_form, "perfil_form": perfil_form},
    )
