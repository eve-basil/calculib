import basil_common.caching as cache

import logging

LOG = logging.getLogger('basil_calculib')

try:
    ENGINE = cache.connect_to_cache()
except KeyError as ex:
    LOG.warning('Missing ENV var: %s', ex.message)
    ENGINE = None
