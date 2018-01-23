from io import BytesIO
from gzip import GzipFile
from zlib import decompressobj, MAX_WBITS
from urllib import request

USER_AGENT = 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'

class Fetcher(object):

    def __init__(self):
        self.opener = self.init_opener()
        self.cache = {}

    def init_opener(self):
        opener = request.build_opener()
        opener.addheaders = [
            ('User-Agent', USER_AGENT),
            ('Accept-Encoding', 'gzip')
        ]
        return opener

    def decompression(self, content, encoding):
        if encoding == 'gzip':
            return GzipFile(fileobj=BytesIO(content), mode='rb').read()
        if encoding == 'deflate':
            return decompressobj(-MAX_WBITS).decompress(content)
        return content

    def download(self, url, data):
        if data:
            resp = self.opener.open(url, data.encode('utf-8'))
        else:
            resp = self.opener.open(url)
        content = resp.read()
        encoding = resp.headers.get('content-encoding', None)
        return self.decompression(content, encoding).decode('UTF-8')

    def open(self, url, force=False, data=None):
        text = self.cache.get(url)
        if force or text is None:
            print('下载 ' + str(url))
            text = self.download(url, data)
            self.cache[url] = text
        return text


fetch = Fetcher().open
