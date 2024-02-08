from django.contrib import admin
from .models import Book
from django.contrib.postgres.search import SearchVector


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'publication_year',
        'average_rating',
        'ratings_count',
        'book_id',
    )
    search_fields = ('title', 'synopsis', 'authors', 'publication_year', 'book_id')
    list_filter = ('publication_year', 'average_rating')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'authors',
                    'publication_year',
                    'average_rating',
                    'ratings_count',
                    'image_url',
                    'book_id',
                )
            },
        ),
        ('Detailed Info', {'classes': ('collapse',), 'fields': ('synopsis',)}),
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            vector = SearchVector('title', 'synopsis', config='english')
            queryset = queryset.annotate(search=vector).filter(search=search_term)
            use_distinct = True
        return queryset, use_distinct
