from django.conf import settings
from django.db import models


class Perfil(models.Model):
    """Datos extra del usuario. Evolución de la clase Autor del blog por consola."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    bio = models.TextField(blank=True)
    especialidad = models.CharField(max_length=100, blank=True)
    redes_sociales = models.CharField(
        max_length=200, blank=True, help_text="Separadas por coma. Ej: @mi_usuario, @otro"
    )
    avatar = models.ImageField("foto de perfil", upload_to="avatares/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    def lista_redes(self):
        return [r.strip() for r in self.redes_sociales.split(",") if r.strip()]
