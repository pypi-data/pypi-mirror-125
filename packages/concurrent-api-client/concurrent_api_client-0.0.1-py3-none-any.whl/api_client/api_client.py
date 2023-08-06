from logging import getLogger, config
import json
import traceback

import asyncio
import functools
import threading
from concurrent.futures import ThreadPoolExecutor

from requests import Request
from requests_toolbelt.utils import dump

from api_client.constants import LOGGING_CONF, API_CLIENT_THREAD_POOL_SIZE, HTTP_STATUS_NO_CONTENT, \
    HTTP_STATUS_UNAUTHORIZED, HTTP_STATUS_FORBIDDEN, HTTP_STATUS_NOT_FOUND, HTTP_STATUS_METHOD_NOT_ALLOWED, \
    HTTP_STATUS_UNPROCESSABLE_ENTITY, HTTP_STATUS_TOO_MANY_REQUEST, HTTP_STATUS_SERVER_ERROR
from api_client.connection_pool_cache import get_httpconnectionpool
from api_client.api_thread_pool import ApiThreadPool
from api_client.exceptions import ApiClientError, ApiAuthenticationError, ApiForbiddenError, \
    ApiNotFoundError, ApiMethodNotAllowedError, ApiUnprocessableEntityError, ApiTooManyRequestsError
from api_client.formatter.util import redact_header


config_dict = None
with open(LOGGING_CONF, 'r', encoding='utf-8') as f:
    config_dict = json.load(f)

config.dictConfig(config_dict)
logger = getLogger(__name__)

class ApiClient:
    """ ApiClient for communicating to knewotn platform over API
    """    

    def __init__(self, ApiFormatter):
        self.api_formatter = ApiFormatter
        self.url = self.api_formatter.get_url()
        self.headers = self.api_formatter.get_headers()
        self.params = self.api_formatter.get_params()

    def get_or_create_eventloop(self):
        """get or create_eventloop

        :return: event_loop
        :rtype: asyncio.get_event_loop
        """        
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()
    
    async def _send(self, prepped, status_no_content=False):
        """async function for sending any API request

        :param prepped: prepped HTTP request
        :type prepped: requests.PreparedRequest
        :param status_no_content: flag for request that is expected to return \
            no-content(204) response, defaults to False
        :type status_no_content: bool, optional
        :raises ApiAuthenticationError: 401 error from platform
        :raises ApiForbiddenError: 403 error from platform
        :raises ApiNotFoundError: 404 error from platform
        :raises ApiMethodNotAllowedError: 405 error from platform
        :raises ApiUnprocessableEntityError: 422 error from platform
        :raises ApiTooManyRequestsError: 429 error from platform
        :raises ApiApiClientError: [description]
        :raises ApiClientError: [description]
        :return: response_json
        :rtype: json
        :return: status
        :rtype: str
        """        

        # Flask supports asyncio but each request to flask ties up to ONE worker even in within a
        # view for background API call. Following async/await code is just for future expansion
        # Ref. https://flask.palletsprojects.com/en/2.0.x/async-await/

        # request_info = '{} url:"{}", data:"{}", headers:"{}"'.format(prepped.method, prepped.url,
        #                                                              prepped.body, prepped.headers)
        request_info = '{} url:"{}", data:"{}", headers:"{}"'.format(prepped.method, prepped.url,
                                                                      prepped.body, 
                                                                      redact_header(prepped.headers))
        logger.debug('Requesting: {}'.format(request_info))

        # TODO: clarify the behavior of ThreadPoolExecutor on web server
        # For server, It might be better to call Executor from singleton instance(?)
        # executor = ApiThreadPool.get_instance()._api_thread_pool_executor
        # loop = self.get_or_create_eventloop()
        # with get_httpconnectionpool(self.url, self.headers) as session:
        #     response = await loop.run_in_executor(executor, functools.partial(session.send,
        #                                                      prepped))
        with ThreadPoolExecutor(max_workers=API_CLIENT_THREAD_POOL_SIZE) as executor:
            loop = self.get_or_create_eventloop()
            with get_httpconnectionpool(self.url, self.headers) as session:
                response = await loop.run_in_executor(executor, functools.partial(session.send,
                                                                                  prepped))

        status = response.status_code
        try:
            # Dump log for HTTP STATUS NO CONTENT (STATUS:204) request
            if (status_no_content):
                data = dump.dump_all(response)
                logger.debug(data.decode('utf-8'))

                if (status == HTTP_STATUS_NO_CONTENT):
                    response_json = {
                        "message (not from API endpoint)": "Event was accepted (status:204)"}
                else:
                    logger.debug(status)
                    response_json = response.json()

            else:
                logger.debug(status)
                response_json = response.json()

            if status == HTTP_STATUS_UNAUTHORIZED:
                raise ApiAuthenticationError(request_info, response_json)
            if status == HTTP_STATUS_FORBIDDEN:
                raise ApiForbiddenError(request_info, response_json)
            elif status == HTTP_STATUS_NOT_FOUND:
                raise ApiNotFoundError(request_info, response_json)
            elif status == HTTP_STATUS_METHOD_NOT_ALLOWED:
                raise ApiMethodNotAllowedError(request_info, response_json)
            elif status == HTTP_STATUS_UNPROCESSABLE_ENTITY:
                raise ApiUnprocessableEntityError(request_info, response_json)
            elif status == HTTP_STATUS_TOO_MANY_REQUEST:
                raise ApiTooManyRequestsError(request_info, response_json)
            elif status == HTTP_STATUS_SERVER_ERROR:
                raise ApiClientError(request_info, response_json)

        except ValueError:
            msg = "Error Send API request. Response is not valid JSON: {}".format(
                response.content)
            logger.exception(msg)
            raise ApiClientError(msg)

        except ApiClientError as e:
            response_json = e.response_json
            # stacktrace for debugging while presenting error status to flask app
            logger.debug(traceback.format_exc())

        logger.debug("Response JSON: {}".format(response_json))
        return response_json, status

    def post(self):
        """post request

        :return: url :rtype: str
        :return: headers :rtype: str
        :return: params :rtype: str
        :return: response_json :rtype: json
        :return: status :rtype: str
        """        
        req = Request('POST', self.url, data=self.params, headers=self.headers)
        prepped = req.prepare()

        loop = self.get_or_create_eventloop()
        response_json, status = loop.run_until_complete(self._send(prepped))

        return self.url, redact_header(self.headers), self.params, response_json, status

    def post_status_no_content(self):
        """post status no content request

        :return: url :rtype: str
        :return: headers :rtype: str
        :return: params :rtype: str
        :return: response_json :rtype: json
        :return: status :rtype: str
        """        
        req = Request('POST', self.url, data=self.params, headers=self.headers)
        prepped = req.prepare()

        loop = self.get_or_create_eventloop()
        response_json, status = loop.run_until_complete(self._send(prepped, status_no_content=True))

        return self.url, redact_header(self.headers), self.params, response_json, status

    def get(self):
        """get request

        :return: url :rtype: str
        :return: headers :rtype: str
        :return: params :rtype: str
        :return: response_json :rtype: json
        :return: status :rtype: str
        """        
        req = Request('GET', self.url, params=self.params, headers=self.headers)
        prepped = req.prepare()

        loop = self.get_or_create_eventloop()
        response_json, status = loop.run_until_complete(self._send(prepped))

        return self.url, redact_header(self.headers), self.params, response_json, status

    def put(self):
        """put request

        :return: url :rtype: str
        :return: headers :rtype: str
        :return: params :rtype: str
        :return: response_json :rtype: json
        :return: status :rtype: str
        """        
        req = Request('PUT', self.url, data=self.params, headers=self.headers)
        prepped = req.prepare()

        loop = self.get_or_create_eventloop()
        response_json, status = loop.run_until_complete(self._send(prepped))

        return self.url, redact_header(self.headers), self.params, response_json, status

    def delete(self):
        """delete request

        :return: url :rtype: str
        :return: headers :rtype: str
        :return: response_json :rtype: json
        :return: status :rtype: str
        """        
        req = Request('DELETE', self.url, headers=self.headers)
        prepped = req.prepare()

        loop = self.get_or_create_eventloop()
        response_json, status = loop.run_until_complete(self._send(prepped))

        return self.url, redact_header(self.headers), response_json, status
