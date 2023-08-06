"""
This module strips unnecessary whitespaces from HTML.
"""


from typing import List
from .libs import minify

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class HTMLStripWhiteSpace(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.ignored_path: List = ["/sitemap.xml"]

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)  # Get response from view function.

        if not response.streaming and not request.path in self.ignored_path:
            content = minify(response.content)
            response.content = content

        return response
