
import urllib.request
import json
import os

# ssl
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

import re
import csv
import sys


class Parser:
    _data = {}
    @classmethod
    def saveToFile(cls, output):
        with open(output, 'w') as fp:
            json.dump(cls._data, fp)

    @classmethod
    def deDiacriticize(cls, s):
        import unicodedata
        ns = unicodedata.normalize('NFKD',s)
        return ''.join([c for c in ns if not unicodedata.combining(c)])
    
    @classmethod
    def parseIntKeys(cls, d):
        return { int(k):v for k,v in d.items() }

    @classmethod
    def getOnlineJson(cls, url, message="<message>"):
        print("Requesting JSON data:", message, file=sys.stderr)
        data = eval( urllib.request.urlopen(url).read() )
        return data
    @classmethod
    def getOnlineJsonList(cls, url, message="<message>"):
        return {int(d['id']):d['name'] for d in cls.getOnlineJson(url, message)}
    




