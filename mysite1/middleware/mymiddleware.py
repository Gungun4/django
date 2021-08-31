from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponse


class MyMW(MiddlewareMixin):

    def process_request(self, request):
        pass

    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass

    def process_response(self, request, response):
        pass

