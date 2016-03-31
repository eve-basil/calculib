import basil_common.caching as cache

try:
    ENGINE = cache.connect_to_cache()
except KeyError as ex:
    ENGINE = None
