from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Perfil


class RegistroForm(UserCreationForm):
    """Formulario de registro de Django (usuario + contraseña dos veces) con estilos de Bootstrap."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"


class UsuarioForm(forms.ModelForm):
    """Datos que vienen del modelo User de Django."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class PerfilForm(forms.ModelForm):
    """Datos propios del perfil (los mismos que tenía la clase Autor del blog por consola)."""

    class Meta:
        model = Perfil
        fields = ["bio", "especialidad", "redes_sociales", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "especialidad": forms.TextInput(attrs={"class": "form-control"}),
            "redes_sociales": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
