from django.middleware.csrf import _get_new_csrf_token
class StaticCache(object):
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        response['server'] =''
        return response
    def process_response(self, request, response):
        request.META["CSRF_COOKIE"] = _get_new_csrf_token()
        if response.path.startswith('/static/'):
            response['server'] =''
            response['Cache-Control'] = ''
            response['Vary'] = ''
            response['Expires'] = ''
        return response