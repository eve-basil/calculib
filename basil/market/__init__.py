import logging
import os
import time

import requests

from basil_common import caching
from basil import ENGINE
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

HEADERS = {'user-agent': 'github.com/eve-basil/calculib[0.1.0-dev]'}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)
# TODO integration tests for all of these

LOG = logging.getLogger(__name__)


def urljoin(*parts):
    url = parts[0]
    for p in parts[1:]:
        if url[-1] != '/':
            url += '/'
        url += p
    return url


def values():
    url = urljoin(crest_base_url(), 'market/prices/')

    def value_provider():
        response = SESSION.get(url)
        code = response.status_code
        if code >= 300:
            LOG.info('Error from [%s] status [%s]', url, code)
            time.sleep(0.05)
            return value_provider()
        items = response.json()['items']
        return {n['type']['id']: n for n in items}

    cache = caching.FactCache(ENGINE, 'crest/mkt/price/', timeout_seconds=900,
                              loader=value_provider)

    def values_cache(type_id):
        found = cache.get(type_id)
        if found and 'averagePrice' in found:
            return found['averagePrice']
        return None

    return values_cache


def names():
    if os.getenv('REFAPI_URL', None):
        url = urljoin(os.getenv('REFAPI_URL'), 'types')
    else:
        default_crest_url = urljoin(crest_base_url(), 'types')
        url = os.getenv('TYPES_URL', default_crest_url)

    @lru_cache()
    def name_provider(type_id):
        name_url = urljoin(url, str(type_id))
        response = SESSION.get(name_url)
        code = response.status_code
        if code >= 300:
            LOG.info('Error from [%s] status [%s]', name_url, code)
            time.sleep(0.05)
            return name_provider(type_id)
        return response.json()['name']
    return name_provider


def prices():
    url = os.getenv('PRICES_URL')

    @lru_cache()
    def price_provider(type_id, name):
        price_url = urljoin(url, str(type_id))
        response = SESSION.get(price_url)
        code = response.status_code
        if code == 404 and WATCHES_FUNC:
            WATCHES_FUNC(type_id, name)
            return None
        elif code >= 300:
            LOG.info('Error from [%s] status [%s]', price_url, code)
            time.sleep(0.05)
            return price_provider(type_id, name)

        return response.json()
    return price_provider


def watches():
    url = os.getenv('WATCHES_URL')

    def watcher(type_id, name):
        watch_url = urljoin(url, str(type_id))
        json = {'name': name}
        response = SESSION.put(watch_url, json=json)
        code = response.status_code
        if code >= 300:
            LOG.info('Error from [%s] status [%s]', watch_url, code)
    return watcher


def crest_base_url():
    return os.getenv('CREST_URL', "https://public-crest.eveonline.com/")


VALUES_FUNC = values()
NAMES_FUNC = names()
PRICES_FUNC = prices()
WATCHES_FUNC = watches()
