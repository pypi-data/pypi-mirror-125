import json
from logging import getLogger

logger = getLogger(__name__)

"""
This module contains all of our exception classes for this project
"""
class ApiClientError(Exception):
    """All package exceptions inherit from this top level exception"""
    err_response_json  = {}
    response_json = {}
    def __init__(self, request_info=None, response_json=None, *args):
        message = "Request Info - {}, Response JSON - {}".format(request_info,
                                                                  json.dumps(response_json))
        if self.err_response_json is not None:
            message = "{}, Error raised by Application - {}".format(message,
                                                                   json.dumps(self.err_response_json))

        # If reponse_json is returned by platform, show it.
        # If not, show application error message in defined subclass
        if response_json is not None:
#            self.response_json = response_json
#        else:
            self.response_json = self.err_response_json

        super().__init__(message, *args)

class ConnectionError(ApiClientError):
    """Thrown if an error occiurs while getting http connection"""
    pass

class ApiAuthenticationError(ApiClientError):
    """Thrown if the user is not authenticated"""
    err_response_json = {
        'Status code': '401',
        'Status': 'Unauthorized',
        'Application message': '(This message is not from API) Please check access token is safely retrieved'
    }

class ApiForbiddenError(ApiAuthenticationError):
    """Thrown if the user is authenticated, but not authorized (does not have permission to do
    this operation)."""
    err_response_json = {
        'Status code': '403',
        'Status': 'Forbidden',
        'Application message': '(This message is not from API) Please check authorization (e.g. registration permission)'
    }

class ApiNotFoundError(ApiClientError):
    """Thrown if the requested resource does not exist."""
    err_response_json = {
        'Status code': '404',
        'Status': 'Not Found',
        'Application message': '(This message is not from API) Requested resource does not exist'
    }

class ApiMethodNotAllowedError(ApiNotFoundError):
    """Thrown if the method used to access the endpoint is incorrect."""
    err_response_json = {
        'Status code': '405',
        'Status': 'Method Not Allowed',
        'Application message': '(This message is not from API) the method used to access the endpoint is incorrect'
    }

class ApiUnprocessableEntityError(ApiClientError):
    """Thrown if some part of the JSON request was ill-formed and could not be parsed,
    or it could be parsed but one of the fields is incorrect"""
    err_response_json = {
        'Status code': '422',
        'Status': 'Unprocessable Entity',
        'Application message': '(This message is not from API)  JSON request was ill-formed and could not be '
                   'parsed, the parsed fields is incorrect or rate limit was exceeded'
    }

class ApiTooManyRequestsError(ApiClientError):
    """Thrown if Rate limit exceeded for this endpoint"""
    err_response_json = {
        'Status code': '429',
        'Status': 'TooManyRequest',
        'Application message': '(This message is not from API) Rate limit was exceeded'
    }

class ApiSystemError(ApiClientError):
    """Thrown if Rate limit exceeded for this endpoint"""
    err_response_json = {
        'Status code': '500',
        'Status': 'Internal Server Error',
        'Application message': '(This message is not from API)  Server Error'
    }
