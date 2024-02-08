import time

from functools import reduce
from operator import add

from django.apps import apps
from django.conf import settings
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    SearchHeadline,
)
from django.db.models import TextField, Value
from django.db.models.functions import Concat


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


class SearchEngine:
    def __init__(self, index_name):
        self.index_name = index_name

    def search(self, params):
        start = time.monotonic()
        config = settings.INSTANTSEARCH_CONFIG[self.index_name]
        model = apps.get_model(config['app_label'], config['model_name'])
        vector = reduce(add, map(SearchVector, config['fields']))
        query = SearchQuery(params['query'])

        concat_fields = [Value(' ')] * (2 * len(config['fields']) - 1)
        concat_fields[0::2] = config['fields']
        objects = (
            model.objects.annotate(
                _rank=SearchRank(vector, query),
                _value=Concat(*concat_fields, output_field=TextField()),
                _headline=SearchHeadline(
                    '_value',
                    params['query'],
                    start_sel=params['highlightPreTag'],
                    stop_sel=params['highlightPostTag'],
                ),
            )
            .filter(_rank__gte=0.001)
            .order_by('-_rank')[:10]
        )

        hits = list(
            map(
                lambda obj: {
                    field: getattr(obj, field, '') for field in config['fields']
                },
                objects,
            )
        )

        for hit, obj in zip(hits, objects):
            hit['_highlightResult'] = {
                'text': {'value': obj._headline, 'matchLevel': 'full'}
            }

        result = {
            'hits': hits,
            'page': 0,
            'nbHits': len(hits),
            'nbPages': 1,
            'hitsPerPage': 10,
            'processingTimeMS': (time.monotonic() - start) * 1000,
            'query': params['query'],
            'params': str(params),
            'index': self.index_name,
        }
        return result

    def search_by_facet(self, facet_name):
        # TODO: `result` is just a placeholder for now
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
        return result


def get_search_engine(index_name):
    config = settings.INSTANTSEARCH_CONFIG[index_name]

    if 'search_engine' not in config:
        return SearchEngine

    module_name, class_name = config['search_engine'].rsplit('.', 1)
    module = __import__(module_name, fromlist=[None])
    class_ = getattr(module, class_name)
    return class_
