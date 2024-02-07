from django.db import models


class Document:
    title = models.CharField(max_length=100)
    content = models.TextField()
