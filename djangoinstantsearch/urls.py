from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:indexName>/query', views.search_index_post, name='search_index_post'),
    path('search/<str:indexName>', views.search_index_get, name='search_index_get'),
    path('search/multiple_indices', views.search_multiple_indices, name='search_multiple_indices'),
    path('search/<str:indexName>/facets/<str:facetName>/query', views.search_for_facet_values, name='search_for_facet_values'),
]
