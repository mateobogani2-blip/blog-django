import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Post

MEDIA_TEMPORAL = tempfile.mkdtemp()


def imagen_de_prueba():
    buffer = BytesIO()
    Image.new("RGB", (40, 30), "steelblue").save(buffer, format="PNG")
    return SimpleUploadedFile("prueba.png", buffer.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class PostTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.autor = User.objects.create_user("autor", password="clave-de-prueba-123")
        self.otro = User.objects.create_user("otro", password="clave-de-prueba-123")
        self.post = Post.objects.create(
            titulo="Primeros pasos con Python", contenido="Contenido de prueba", autor=self.autor
        )

    def test_lista_y_detalle_sin_imagen(self):
        respuesta = self.client.get(reverse("posts:lista"))
        self.assertContains(respuesta, "Primeros pasos con Python")
        self.assertContains(respuesta, "sin-imagen.svg")
        respuesta = self.client.get(self.post.get_absolute_url())
        self.assertEqual(respuesta.status_code, 200)

    def test_anonimo_no_puede_crear_editar_ni_eliminar(self):
        for nombre, args in [("crear", []), ("editar", [self.post.pk]), ("eliminar", [self.post.pk])]:
            url = reverse(f"posts:{nombre}", args=args)
            respuesta = self.client.get(url)
            self.assertRedirects(respuesta, f"{reverse('usuarios:login')}?next={url}")
        self.client.post(reverse("posts:eliminar", args=[self.post.pk]))
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_crear_post_con_imagen(self):
        self.client.login(username="autor", password="clave-de-prueba-123")
        respuesta = self.client.post(
            reverse("posts:crear"),
            {"titulo": "Con imagen", "contenido": "Hola", "tags": "Django", "estado": "publicado",
             "imagen": imagen_de_prueba()},
        )
        post = Post.objects.get(titulo="Con imagen")
        self.assertRedirects(respuesta, post.get_absolute_url())
        self.assertEqual(post.autor, self.autor)
        self.assertTrue(post.imagen.name.startswith("posts/"))
        self.assertContains(self.client.get(post.get_absolute_url()), post.imagen.url)

    def test_editar_y_eliminar_propio(self):
        self.client.login(username="autor", password="clave-de-prueba-123")
        self.client.post(
            reverse("posts:editar", args=[self.post.pk]),
            {"titulo": "Título nuevo", "contenido": "Nuevo", "tags": "", "estado": "publicado"},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, "Título nuevo")
        self.client.post(reverse("posts:eliminar", args=[self.post.pk]))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_otro_usuario_no_puede_editar_ni_eliminar(self):
        self.client.login(username="otro", password="clave-de-prueba-123")
        respuesta = self.client.get(reverse("posts:editar", args=[self.post.pk]))
        self.assertEqual(respuesta.status_code, 404)
        self.client.post(reverse("posts:eliminar", args=[self.post.pk]))
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_borrador_solo_lo_ve_el_autor(self):
        borrador = Post.objects.create(titulo="Borrador", contenido="x", autor=self.autor,
                                       estado=Post.Estado.BORRADOR)
        self.assertEqual(self.client.get(borrador.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse("posts:lista")), "Borrador")
        self.client.login(username="autor", password="clave-de-prueba-123")
        self.assertEqual(self.client.get(borrador.get_absolute_url()).status_code, 200)

    def test_busqueda(self):
        respuesta = self.client.get(reverse("posts:lista"), {"q": "python"})
        self.assertContains(respuesta, "Primeros pasos con Python")
        respuesta = self.client.get(reverse("posts:lista"), {"q": "contenido de prueba"})
        self.assertContains(respuesta, "Primeros pasos con Python")
        respuesta = self.client.get(reverse("posts:lista"), {"q": "zzz"})
        self.assertContains(respuesta, "No se encontraron posts")

    def test_paginacion_mantiene_la_busqueda(self):
        for numero in range(8):
            Post.objects.create(titulo=f"Django {numero}", contenido="x", autor=self.autor)
        respuesta = self.client.get(reverse("posts:lista"), {"q": "django"})
        self.assertContains(respuesta, "?q=django&amp;page=2")
