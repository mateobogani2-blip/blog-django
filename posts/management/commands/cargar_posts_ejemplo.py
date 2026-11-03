"""Carga los posts de ejemplo del blog por consola (posts_ejemplo.json).

Uso: python manage.py cargar_posts_ejemplo
"""
import json
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from posts.models import Post

ARCHIVO = Path(__file__).resolve().parent.parent.parent / "datos" / "posts_ejemplo.json"


class Command(BaseCommand):
    help = "Crea un usuario de ejemplo y carga los posts del blog por consola."

    def handle(self, *args, **options):
        with open(ARCHIVO, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        creados = 0
        for item in datos:
            autor_datos = item["autor"]
            username = autor_datos["nombre"].lower().replace(" ", "_")
            usuario, nuevo = User.objects.get_or_create(username=username)
            if nuevo:
                # Sin contraseña usable: es solo un autor de ejemplo
                usuario.set_unusable_password()
                partes = autor_datos["nombre"].split(" ", 1)
                usuario.first_name = partes[0]
                usuario.last_name = partes[1] if len(partes) > 1 else ""
                usuario.save()
                perfil = usuario.perfil
                perfil.bio = autor_datos.get("bio", "")
                perfil.especialidad = autor_datos.get("especialidad", "")
                perfil.redes_sociales = ", ".join(autor_datos.get("redes_sociales", []))
                perfil.save()

            _, post_nuevo = Post.objects.get_or_create(
                titulo=item["titulo"],
                autor=usuario,
                defaults={
                    "contenido": item["contenido"],
                    "tags": ", ".join(item.get("tags", [])),
                    "estado": item.get("estado", Post.Estado.PUBLICADO),
                },
            )
            creados += post_nuevo

        self.stdout.write(self.style.SUCCESS(f"Listo: {creados} posts de ejemplo cargados."))
