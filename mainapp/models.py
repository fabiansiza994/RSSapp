from django.db import models

# Create your models here.
class CreateRss(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titulo")
    url = models.TextField(verbose_name="Rss Url")
    public = models.BooleanField(verbose_name="Publico?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")
