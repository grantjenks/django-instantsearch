from django.urls import path
from . import views

urlpatterns = [
    path('1/indexes/<str:indexName>/query', views.search_index_post, name='search_index_post'),
    path('1/indexes/<str:indexName>', views.search_index_get, name='search_index_get'),
    path('1/indexes/*/queries', views.search_multiple_indices, name='search_multiple_indices'),
    path('1/indexes/<str:indexName>/facets/<str:facetName>/query', views.search_for_facet_values, name='search_for_facet_values'),
]
