import json

from urllib.parse import unquote

from django.http import JsonResponse, QueryDict
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


EXAMPLE_SEARCH_RESULTS = {
    'index1': {
        'hits': [
            {
                'name': 'Betty Jane Mccamey',
                'company': 'Vita Foods Inc.',
                'email': 'betty@mccamey.com',
                'objectID': '6891Y2usk0',
                '_highlightResult': {
                    'name': {
                        'value': 'Betty <b>Jan</b>e Mccamey',
                        'matchLevel': 'full',
                    },
                    'company': {'value': 'Vita Foods Inc.', 'matchLevel': 'none'},
                    'email': {'value': 'betty@mccamey.com', 'matchLevel': 'none'},
                },
            },
        ],
        'page': 0,
        'nbHits': 1,
        'nbPages': 1,
        'hitsPerPage': 20,
        'processingTimeMS': 1,
        'query': 'van',
        'params': 'query=van',
        'index': 'index1',
    },
    'index2': {
        'hits': [
            {
                'name': 'Gayla Geimer Dan',
                'company': 'Ortman Mccain Co',
                'email': 'gayla@geimer.com',
                'objectID': 'ap78784310',
                '_highlightResult': {
                    'name': {'value': 'Gayla Geimer <b>Dan</b>', 'matchLevel': 'full'},
                    'company': {'value': 'Ortman Mccain Co', 'matchLevel': 'none'},
                    'email': {'highlighted': 'gayla@geimer.com', 'matchLevel': 'none'},
                },
            }
        ],
        'page': 0,
        'nbHits': 1,
        'nbPages': 1,
        'hitsPerPage': 20,
        'processingTimeMS': 1,
        'query': 'van',
        'params': 'query=van',
        'index': 'index2',
    },
    'YourIndexName': {
        'hits': [
            {
                'name': 'George Clooney',
                'objectID': '2051967',
                '_highlightResult': {
                    'name': {
                        'value': '__ais-highlight__George__/ais-highlight__ __ais-highlight__Clo__/ais-highlight__oney',
                        'matchLevel': 'full',
                    }
                },
                '_snippetResult': {
                    'bio': {
                        'value': 'is the son of __ais-highlight__George__/ais-highlight__ __ais-highlight__Clo__/ais-highlight__oney as was his father'
                    }
                },
                '_rankingInfo': {
                    'nbTypos': 0,
                    'firstMatchedWord': 0,
                    'proximityDistance': 1,
                    'userScore': 5,
                    'geoDistance': 0,
                    'geoPrecision': 1,
                    'nbExactWords': 0,
                },
            },
            {
                'name': "George Clooney's Irish Roots",
                'year': '(2012 Documentary)',
                'objectID': '825416',
                '_highlightResult': {
                    'name': {
                        'value': "__ais-highlight__George__/ais-highlight__ __ais-highlight__Clo__/ais-highlight__oney's Irish Roots",
                        'matchLevel': 'full',
                    },
                    'year': {'value': '(2012 Documentary)', 'matchLevel': 'none'},
                },
                '_rankingInfo': {
                    'nbTypos': 0,
                    'firstMatchedWord': 0,
                    'proximityDistance': 1,
                    'userScore': 4,
                    'geoDistance': 0,
                    'geoPrecision': 1,
                    'nbExactWords': 0,
                },
            },
        ],
        'page': 0,
        'nbHits': 38,
        'nbPages': 19,
        'hitsPerPage': 2,
        'processingTimeMS': 6,
        'query': 'george clo',
        'parsedQuery': 'george clo',
        'params': 'query=george%20clo&hitsPerPage=2&getRankingInfo=1',
    },
}


@csrf_exempt
@require_http_methods(['POST'])
def search_index_post(request, index_name):
    """
    Endpoint to search within a single index using POST method.
    """
    # TODO
    # result = EXAMPLE_SEARCH_RESULTS[index_name]
    # return JsonResponse(result, status=200)
    raise NotImplementedError


@require_http_methods(['GET'])
def search_index_get(request, index_name):
    """
    Endpoint to search within a single index using GET method.
    """
    raise NotImplementedError


def search_index(index_name, params):
    for key in params:
        print(key, params[key])
    result = EXAMPLE_SEARCH_RESULTS[index_name]
    return result


@csrf_exempt
@require_http_methods(['POST'])
def search_multiple_indices(request):
    """
    Endpoint to search across multiple indices in a single API call.
    """
    body = json.loads(request.body.decode())
    results = {'results': []}
    for search in body['requests']:
        params = QueryDict(unquote(search['params']))
        result = search_index(search['indexName'], params)
        results['results'].append(result)
    return JsonResponse(results, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def search_for_facet_values(request, index_name, facet_name):
    """
    Endpoint to search for specific facet values within an index.
    """
    result = {
        'facetHits': [
            {
                'value': 'Mobile phones',
                'highlighted': 'Mobile __ais-highlight__phone__/ais-highlight__s',
                'count': 507,
            },
            {
                'value': 'Phone cases',
                'highlighted': '__ais-highlight__Phone__/ais-highlight__ cases',
                'count': 63,
            },
        ]
    }
    return JsonResponse(result, status=200)
