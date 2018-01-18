from rest_framework.settings import api_settings


class APIVersionHeaderMiddleware(object):
    """
    The DSO specifies that the full API version should be in the response headers. For now, the major API version is
    the full API version.
    """
    version_param = api_settings.VERSION_PARAM

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            r = request.resolver_match
            if r.namespace == 'api' and self.version_param in r.kwargs:
                response['API-Version'] = r.kwargs[self.version_param]
        except:
            pass

        return response
