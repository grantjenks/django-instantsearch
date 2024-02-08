import json

from urllib.parse import unquote

from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .core import get_search_engine


@csrf_exempt
@require_http_methods(['POST'])
def search_index_post(request, index_name):
    """Search within a single index using POST method."""
    body = json.loads(request.body.decode())
    params = QueryDict(unquote(body['params']))
    class_ = get_search_engine(index_name)
    engine = class_(index_name)
    result = engine.search(params)
    return JsonResponse(result, status=200)


@require_http_methods(['GET'])
def search_index_get(request, index_name):
    """Search within a single index using GET method."""
    params = request.GET
    class_ = get_search_engine(index_name)
    engine = class_(index_name)
    result = engine.search(params)
    return JsonResponse(result, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def search_multiple_indices(request):
    """Search across multiple indices in a single API call."""
    body = json.loads(request.body.decode())
    results = {'results': []}
    for search in body['requests']:
        params = QueryDict(unquote(search['params']))
        index_name = search['indexName']
        class_ = get_search_engine(index_name)
        engine = class_(index_name)
        result = engine.search(params)
        results['results'].append(result)
    return JsonResponse(results, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def search_for_facet_values(request, index_name, facet_name):
    """Search for specific facet values within an index."""
    class_ = get_search_engine(index_name)
    engine = class_(index_name)
    result = engine.search_by_facet(facet_name)
    return JsonResponse(result, status=200)
