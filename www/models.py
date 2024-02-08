from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = JSONField()
    publication_year = models.IntegerField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    image_url = models.URLField(max_length=1024)
    ratings_count = models.BigIntegerField()
    synopsis = models.TextField()

    class Meta:
        indexes = [
            GinIndex(
                SearchVector('title', 'synopsis', config='english'),
                name='book_search_vector_index',
            ),
        ]

    def __str__(self):
        return self.title
