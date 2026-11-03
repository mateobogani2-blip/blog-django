from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Formulario para crear y editar posts. El autor no se pide: es el usuario logueado."""

    class Meta:
        model = Post
        fields = ["titulo", "contenido", "imagen", "tags", "estado"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "tags": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }
