from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    """Publicación del blog. Evolución de la clase Post del blog por consola."""

    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADO = "publicado", "Publicado"
        ARCHIVADO = "archivado", "Archivado"

    titulo = models.CharField("título", max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="posts/", blank=True, null=True)
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Separados por coma. Ej: Python, Django, Web",
    )
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PUBLICADO)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.titulo} | Autor: {self.autor} | Estado: {self.estado}"

    def get_absolute_url(self):
        return reverse("posts:detalle", args=[self.pk])

    def lista_tags(self):
        """Devuelve los tags como lista, sin espacios ni vacíos."""
        return [t.strip() for t in self.tags.split(",") if t.strip()]
