""" A simple HTTP session cache. """
from contextlib import contextmanager
import urllib.parse
import requests
from logging import getLogger

from api_client.constants import API_CONNECTION_POOL_SIZE
from api_client.exceptions import ConnectionError
logger = getLogger(__name__)

_SESSION_CACHE = {}

def patch_https_connection_pool(**constructor_kwargs):
    """
    This allows to override the default parameters of the
    HTTPConnectionPool constructor.
    For example, to increase the poolsize to fix problems
    with "HttpSConnectionPool is full, discarding connection"
    call this function with maxsize=16 (or whatever size
    you want to give to the connection pool)
    """
    from urllib3 import connectionpool, poolmanager

    class MyHTTPSConnectionPool(connectionpool.HTTPSConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPSConnectionPool, self).__init__(*args,**kwargs)
    poolmanager.pool_classes_by_scheme['https'] = MyHTTPSConnectionPool

@contextmanager
def get_httpconnectionpool(url, headers):
    """
    Get a contextmanager that yields a Session.

    :param str url: the url that we are requesting
    :param dict headers: the headers that we are requesting
    :yield requests.Session: the session
    """

    # Sessions are unique per (host, port, authorization in header).
    url_split = urllib.parse.urlsplit(url)
    key = (url_split.hostname, url_split.port)
    if headers:
        auth = headers['Authorization']
    else:
        auth = 'no-auth'
    key = "{}-{}".format(key, auth)

    if key in _SESSION_CACHE:
        session = _SESSION_CACHE[key]
    else:
        patch_https_connection_pool(maxsize=API_CONNECTION_POOL_SIZE)
        session = requests.Session()

    _SESSION_CACHE[key] = session
    # On any excption, invalidate the cache entry.

    try:
        yield session
    except (requests.ConnectionError, requests.Timeout) as err:
        if key in _SESSION_CACHE and _SESSION_CACHE[key] is session:
            del _SESSION_CACHE[key]
        session.close()
        raise ConnectionError(str(err))
