import urllib.parse
from json import dumps

def make_body(self, content):
    """Return content as bytearray accepted body of SIS HTTP API request.
    """
    if isinstance(content, bytearray):
        return bytearray(content)
    if isinstance(content, str):
        return bytearray(content.encode('utf-8'))
    if isinstance(content, dict):
        return bytearray(dumps(content).encode('utf-8'))
    return bytearray(content)

def make_url(self, url, params=None):
    """Creates valid URL with new query string parameters or
    appended to existing query string.
    """
    parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(parts[4]))
    if params:
        query.update(params)
    parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(parts)