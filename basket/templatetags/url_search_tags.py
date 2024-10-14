from django import template
from urllib.parse import urlparse

register = template.Library()


@register.simple_tag()
def find_search_url(request):
    url = request.headers.get("Referer")
    parsed_url = urlparse(url)
    path = parsed_url.path
    return path
