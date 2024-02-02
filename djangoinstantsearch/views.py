from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["POST"])
def search_index_post(request, indexName):
    """
    Endpoint to search within a single index using POST method.
    """
    # Implement the logic here
    return JsonResponse({"message": "Search results from POST method"}, status=200)


@require_http_methods(["GET"])
def search_index_get(request, indexName):
    """
    Endpoint to search within a single index using GET method.
    """
    # Implement the logic here
    return JsonResponse({"message": "Search results from GET method"}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def search_multiple_indices(request):
    """
    Endpoint to search across multiple indices in a single API call.
    """
    # Implement the logic here
    return JsonResponse({"message": "Results from searching multiple indices"}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def search_for_facet_values(request, indexName, facetName):
    """
    Endpoint to search for specific facet values within an index.
    """
    # Implement the logic here
    return JsonResponse({"message": "Facet search results"}, status=200)
