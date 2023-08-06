class ApiFormatter:
    """ a template formatter base for building  API request
    """    
    def __init__(self, url=None, path=None, token=None):
        self.url = url
        self.path = path
        self.token = token

    def get_url(self):
        pass

    # Default header with "Authorization: Bearer" is generated here in super class.
    # If an API does not expect this header format, Formatter subclass can override get_header()
    def get_headers(self):
        if self.token :
            headers = {
                "Authorization": "Bearer {}".format(self.token),
                "content-type": "application/json"
            }
            return headers
        else:
            pass

    def get_params(self):
        pass
