from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UsuariosTests(TestCase):
    def test_registro_crea_usuario_perfil_e_inicia_sesion(self):
        respuesta = self.client.post(
            reverse("usuarios:registro"),
            {"username": "nuevo", "email": "", "password1": "UnaClaveSegura.2026",
             "password2": "UnaClaveSegura.2026"},
        )
        self.assertRedirects(respuesta, reverse("posts:lista"))
        usuario = User.objects.get(username="nuevo")
        self.assertTrue(hasattr(usuario, "perfil"))
        self.assertContains(self.client.get(reverse("posts:lista")), "Hola, nuevo")

    def test_login_y_logout(self):
        User.objects.create_user("ana", password="clave-de-prueba-123")
        respuesta = self.client.post(
            reverse("usuarios:login"), {"username": "ana", "password": "clave-de-prueba-123"}
        )
        self.assertRedirects(respuesta, reverse("posts:lista"))
        self.client.post(reverse("usuarios:logout"))
        self.assertContains(self.client.get(reverse("posts:lista")), "Iniciar sesión")

    def test_editar_perfil_requiere_login(self):
        url = reverse("usuarios:editar_perfil")
        respuesta = self.client.get(url)
        self.assertRedirects(respuesta, f"{reverse('usuarios:login')}?next={url}")

    def test_editar_perfil(self):
        User.objects.create_user("ana", password="clave-de-prueba-123")
        self.client.login(username="ana", password="clave-de-prueba-123")
        self.client.post(
            reverse("usuarios:editar_perfil"),
            {"first_name": "Ana", "last_name": "", "email": "", "bio": "Hola",
             "especialidad": "Python", "redes_sociales": "@ana"},
        )
        respuesta = self.client.get(reverse("usuarios:perfil", args=["ana"]))
        self.assertContains(respuesta, "Python")
        self.assertContains(respuesta, "@ana")
