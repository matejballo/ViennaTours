import re
from django.conf import settings
from django.contrib.auth.decorators import login_required

class ClassName(object):

    def __init__(self, response):
        self.get_response = response
        self.required = tuple(re.compile(url) for url in settings.AUTH_URLS)
        self.exceptions = tuple(re.compile(url)for url in settings.NO_AUTH_URLS)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            return None
    
        for url in self.required:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)
        return None
