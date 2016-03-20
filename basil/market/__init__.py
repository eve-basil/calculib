import os

import requests

from basil_common import caching

HEADERS = {'user-agent': 'github.com/eve-basil/calculib[0.1.0-dev]'}
# TODO integration tests for all of these


def values():
    url = '/'.join([crest_base_url(), 'market/prices/'])

    def avg_from(json, type_id):
        return next(item['averagePrice'] for item in json['items']
                    if item['type']['id'] == type_id)

    def value_provider():
        return requests.get(url, headers=HEADERS).json()

    if caching.ENGINE:
        cache = caching.FactCache(caching.ENGINE, 'crest/', 900,
                                  value_provider)

    def values_cache(type_id):
        return avg_from(cache.get('market/prices/'), type_id)

    return values_cache


def names():
    url = os.getenv('TYPES_URL', '/'.join([crest_base_url(), 'types']))

    def name_provider(type_id):
        return requests.get('/'.join([url, type_id]),
                            headers=HEADERS).json()['name']
    return name_provider


def prices():
    url = os.getenv('PRICES_URL')

    def price_provider(type_id):
        return requests.get('/'.join([url, type_id]), headers=HEADERS).json()
    return price_provider


def crest_base_url():
    return os.getenv('CREST_URL', "https://public-crest.eveonline.com")


VALUES_FUNC = values()
NAMES_FUNC = names()
PRICES_FUNC = prices()
