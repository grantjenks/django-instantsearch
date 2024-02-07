# Django InstantSearch

Django InstantSearch is a Django app that implements just enough of the Algolia
Search API to work with
[instantsearch.js](https://www.algolia.com/doc/guides/building-search-ui/what-is-instantsearch/js/).


# Developer Docs

1. python manage.py runserver_plus --cert /tmp/cert/cert.crt

2. Open https://127.0.0.1:8000/ in Chrome Incognito window


# Algolia Search API Docs

Search index (POST)#
A

Path: /1/indexes/{indexName}/query
HTTP Verb: POST
Required API Key: any key with the search ACL

Description:

Return objects that match the query.

You can find the list of parameters that you can use in the POST body in the Search Parameters section.

Alternatively, parameters may be specified as a URL-encoded query string inside the params attribute.

This method has a constant URL, thus allowing the web browser to cache Cross-Origin Resource Sharing (CORS) OPTION requests.

Parameters:

Parameter	Description
params#
type: URL-encoded string
default: "" (no search parameters)
Optional
Search parameters

Errors:

400: Bad request or request argument
404: Index does not exist
Example:

A


Shell
Copy
curl -X POST \
     -H "X-Algolia-API-Key: ${API_KEY}" \
     -H "X-Algolia-Application-Id: ${APPLICATION_ID}" \
     --data-binary '{ "params": "query=george%20clo&hitsPerPage=2&getRankingInfo=1" }' \
     "https://${APPLICATION_ID}-dsn.algolia.net/1/indexes/imdb/query"
When the query is successful, the HTTP response is a 200 OK and returns the list of results in the hits attribute of the returned JSON object:


JSON
Copy
{
    "hits": [
        {
            "name": "George Clooney",
            "objectID": "2051967",
            "_highlightResult": {
                "name": {
                    "value": "<em>George</em> <em>Clo</em>oney",
                    "matchLevel": "full"
                }
            },
            "_snippetResult": {
                "bio": {
                    "value": "is the son of <em>George</em> <em>Clo</em>oney as was his father"
                }
            },
            "_rankingInfo": {
                "nbTypos": 0,
                "firstMatchedWord": 0,
                "proximityDistance": 1,
                "userScore": 5,
                "geoDistance": 0,
                "geoPrecision": 1,
                "nbExactWords": 0
            }
        },
        {
            "name": "George Clooney's Irish Roots",
            "year": "(2012 Documentary)",
            "objectID": "825416",
            "_highlightResult": {
                "name": {
                    "value": "<em>George</em> <em>Clo</em>oney's Irish Roots",
                    "matchLevel": "full"
                },
                "year": {
                    "value": "(2012 Documentary)",
                    "matchLevel": "none"
                }
            },
            "_rankingInfo": {
                "nbTypos": 0,
                "firstMatchedWord": 0,
                "proximityDistance": 1,
                "userScore": 4,
                "geoDistance": 0,
                "geoPrecision": 1,
                "nbExactWords": 0
            }
        }
    ],
    "page": 0,
    "nbHits": 38,
    "nbPages": 19,
    "hitsPerPage": 2,
    "processingTimeMS": 6,
    "query": "george clo",
    "parsedQuery": "george clo",
    "params": "query=george%20clo&hitsPerPage=2&getRankingInfo=1"
}
Search index (GET)#
A

Path: /1/indexes/{indexName}
HTTP Verb: GET
Required API Key: any key with the search ACL

Description:

You can also query an index with a GET request.

The GET method’s URL varies with the search parameters, and thus forces the browser to perform one Cross-Origin Resource Sharing (CORS) OPTION request for each query, without any way to cache them. Its use is therefore discouraged.

Parameters#
You can pass any of the Search Parameters in the URL’s query string.

Errors:

400: Bad request or request argument
404: Index does not exist
Example:

A


Shell
Copy
curl -X GET \
     -H "X-Algolia-API-Key: ${API_KEY}" \
     -H "X-Algolia-Application-Id: ${APPLICATION_ID}" \
    "https://${APPLICATION_ID}-dsn.algolia.net/1/indexes/imdb?query=george%20clo&hitsPerPage=2&getRankingInfo=1"
Search multiple indices#
A

Path: /1/indexes/*/queries
HTTP Verb: POST
Required API Key: any key with the search ACL

Description:

This method allows to send multiple search queries, potentially targeting multiple indices, in a single API call.

Parameters:

Parameter	Description
requests#
type: list
Required
A list of queries. Results will be received in the same order as the queries in the requests attribute.

Each query is described by the following attributes:

indexName: index targeted by the query;
params: URL-encoded list of search parameters.
strategy#
type: string
default: "none"
Optional
Allows optimizing execution of the queries by potentially skipping some of them.

The following values are allowed:

none: Execute all queries.

stopIfEnoughMatches: Execute queries one by one, but stop as soon as one query matches at least as many hits as its hitsPerPage parameter. More formally: query N is executed only if all of queries 0 through N-1 had strictly less hits than their requested number of hits per page.

Let’s illustrate stopIfEnoughMatches: Let’s say you send 3 queries with hitsPerPage set to 50, 5 and 20 (respectively). There are different possible scenarios:

Run query #1
50+ hits are found: skip to step 4
otherwise: continue with query #2
Run query #2
5+ hits where found: skip to step 4
otherwise: continue with query #3
Run query #3
This is the last query, so we don’t care about its outcome
Return results
Return actual results for queries that were processed
Return empty hits for queries that were skipped, along with a processed attribute set to false
Errors:

400: Bad request argument
404: Index does not exist
Example:

A


Shell
Copy
curl -X POST \
     -H "X-Algolia-API-Key: ${API_KEY}" \
     -H "X-Algolia-Application-Id: ${APPLICATION_ID}" \
     --data-binary '{ "requests": [
                        { "indexName": "index1", "params": "query=van" },
                        { "indexName": "index2", "params": "query=van" }
                      ],
                      "strategy": "none"
                    }' \
    "https://${APPLICATION_ID}-dsn.algolia.net/1/indexes/*/queries"
When queries are successful, the HTTP response is a 200 OK and returns all results:


JSON
Copy
{
  "results":[
    {
      "hits":[
        {
          "name": "Betty Jane Mccamey",
          "company": "Vita Foods Inc.",
          "email": "betty@mccamey.com",
          "objectID": "6891Y2usk0",
          "_highlightResult": {
              "name": {"value": "Betty <b>Jan</b>e Mccamey", "matchLevel": "full"},
              "company": {"value": "Vita Foods Inc.", "matchLevel": "none"},
              "email": {"value": "betty@mccamey.com", "matchLevel": "none"}
          }
        }],
      "page": 0,
      "nbHits": 1,
      "nbPages": 1,
      "hitsPerPage": 20,
      "processingTimeMS": 1,
      "query": "van",
      "params": "query=van",
      "index": "index1"
    },
    {
      "hits": [
        {
          "name": "Gayla Geimer Dan",
          "company": "Ortman Mccain Co",
          "email": "gayla@geimer.com",
          "objectID": "ap78784310"
          "_highlightResult": {
            "name": {"value": "Gayla Geimer <b>Dan</b>", "matchLevel": "full" },
            "company": {"value": "Ortman Mccain Co", "matchLevel": "none" },
            "email": {"highlighted": "gayla@geimer.com", "matchLevel": "none" }
          }
        }],
      "page": 0,
      "nbHits": 1,
      "nbPages": 1,
      "hitsPerPage": 20,
      "processingTimeMS": 1,
      "query": "van",
      "params": "query=van",
      "index": "index2"
    }
  ]
}
Search for facet values#
A

Path: /1/indexes/{indexName}/facets/{facetName}/query
HTTP Verb: POST
Required API Key: any key with the search ACL

Description:

Search for values of a given facet, optionally restricting the returned values to those contained in objects matching other search criteria.

Pagination isn’t supported (page and hitsPerPage parameters are ignored). By default, the engine returns a maximum of 10 values. You can adjust with maxFacetHits.

Parameters:

Parameter	Description
params#
type: URL-encoded query string
default: ""
Optional
Search parameters. You may use this parameter to specify parameters specific to this endpoint. You may also specify any number of other regular search parameters. They will apply to objects in the index.

facetQuery#
type: string
default: ""
Optional
Text to search inside the facet’s values.

maxFacetHits#
type: integer
default: 10
Optional
The maximum number of facet hits to return.

For performance reasons, the maximum allowed number of returned values is 100.

Errors:

400: Attribute facetName isn’t in attributesForFaceting, or not with the searchable() specifier
404: Index indexName doesn’t exist
Example:

A


Shell
Copy
curl -X POST \
     -H "X-Algolia-API-Key: ${API_KEY}" \
     -H "X-Algolia-Application-Id: ${APPLICATION_ID}" \
     --data-binary "{\"params\": \"facetQuery=${facetQuery}\"}" \
    "https://${APPLICATION_ID}.algolia.net/1/indexes/${indexName}/facets/${facetName}/query"
When the query is successful, the HTTP response is a 200 OK. It contains values that match the queried text, and that are contained in at least one object matching the other search parameters.

The response body contains the following fields:

facetHits (array): Matched values. Each hit contains the following fields:
value (string): Raw value of the facet
highlighted (string): Highlighted facet value
count (integer): How many objects contain this facet value. This takes into account the extra search parameters specified in the query. Like for a regular search query, the counts may not be exhaustive. See the related discussion.
Values are sorting by decreasing frequency.


JSON
Copy
{
    "facetHits": [
        {
            "value": "Mobile phones",
            "highlighted": "Mobile <em>phone</em>s",
            "count": 507
        },
        {
            "value": "Phone cases",
            "highlighted": "<em>Phone</em> cases",
            "count": 63
        }
    ]
}
