from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "estado", "creado")
    list_filter = ("estado", "creado")
    search_fields = ("titulo", "contenido", "tags")
