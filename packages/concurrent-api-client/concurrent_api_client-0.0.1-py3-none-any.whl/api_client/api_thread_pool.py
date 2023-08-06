from logging import getLogger
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

from api_client.constants import API_CLIENT_THREAD_POOL_SIZE

logger = getLogger(__name__)


class ApiThreadPool(object):
    """ApiThreadPool: Singleton class for managing ThreadPoolExecutor (for future expansion)

    :param object: 
    :type object: object
    :raises NotImplementedError: error thrown if constructor is directly called
    :return: cls._unique_instance
    :rtype: ApiThreadPool
    """    

    _unique_instance = None
    _lock = Lock()
    _api_thread_pool_executor = None

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            with cls._lock:
                if not cls._unique_instance:
                    cls._unique_instance = cls.__internal_new__()
                    cls._api_thread_pool_executor = ThreadPoolExecutor(
                    max_workers=API_CLIENT_THREAD_POOL_SIZE)
                    cls._api_thread_pool_executor.submit(logger.debug("Thread pool is generated"))
        return cls._unique_instance