
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


class Kraje(Parser):
    @classmethod
    def readFromServer(cls):
        cls._data = cls.getOnlineJsonList('https://b2c.cpost.cz/services/Address/getRegionListAsJson', 'seznam kraju')
        return cls._data
    @classmethod
    def readFromFile(cls):
        with open('kraje.json','r') as f:
            cls._data = cls.parseIntKeys( json.load(f) )
    @classmethod
    def saveToFile(cls, output="kraje.json"):
        super().saveToFile(output)

    @classmethod
    def get(cls, key=None):
        if key == None:
            return cls._data
        elif isinstance(key,str):
            for k,v in cls._data.items():
                if cls.deDiacriticize(v.lower()) == cls.deDiacriticize(key.lower()):
                    return k
        elif isinstance(key,int):
            return cls._data[key]
        raise KeyError
    def __getitem__(self, key):
        return self.get(key)    
    
    @classmethod
    def setup(cls):
        try:
            cls.readFromFile()
        except:
            cls.readFromServer()
            cls.saveToFile()
    
    @classmethod
    def iterate(cls):
        for kraj,name in cls._data.items():
            yield kraj
    def __next__(self):
        return [i for i in self.iterate()]
    def __iter__(self):
        return [i for i in self.iterate()].__iter__()
Kraje.setup()

class Obce(Parser):
    @classmethod
    def readFromServer(cls, kraj=None):
        # get regions
        kraje = Kraje()
        # suppose kraj parameter (only obce from kraj)
        if kraj is not None:
            try:
                kraje = [int(kraj)]
            except:
                kraj = Kraje.get(kraj)
        # read okresy
        for kraj in kraje:
            rqurl = 'https://b2c.cpost.cz/services/Address/getDistrictListAsJson?id=' + str(kraj)
            okresy = cls.getOnlineJson(rqurl, "okresy kraje "+Kraje.get(kraj))
            # read obce
            obce = {}
            for okres in okresy:
                rqurl = 'https://b2c.cpost.cz/services/Address/getCityListAsJson?id=' + str(okres['id'])
                obceOkresu = cls.getOnlineJson(rqurl, "obce okresu "+okres['name'])
                # merge obce
                for obec in obceOkresu:
                    obce[ int(obec['id']) ] = obec['name']
            # write into global
            cls._data[kraj] = obce
        return cls._data
    @classmethod
    def readFromFile(cls):
        with open('obce.json','r') as f:
            cls._data = cls.parseIntKeys( json.load(f) )
            return cls._data

    @classmethod
    def saveToFile(cls, output="obce.json"):
        super().saveToFile(output)
    @classmethod
    def setup(cls):
        try:
            cls.readFromFile()
        except:
            cls.readFromServer()
            cls.saveToFile()
    
    @classmethod
    def get(cls, key=None, kraj=None):
        with open('obce.json','r') as f:
            obce = cls.parseIntKeys( json.load(f) ) # all obce
            print(obce[1])
            if key == None:
                return obce
            elif isinstance(key,int): # obec ID
                kraje = Kraje()
                if kraj is not None:
                    kraje = Kraje.get(kraj)
                for kraj in kraje:
                    try:
                        return obce[kraj][key]
                    except:
                        pass
                    else:
                        raise KeyError
            elif isinstance(key, str): # obec name
                obceOfName = []
                kraje = Kraje()
                if kraj is not None:
                    kraje = Kraje.get(kraj)
                for kraj in kraje:
                    for obecID, obecName in obce[kraj].items():
                        if cls.deDiacriticize(obecName.lower()) == cls.deDiacriticize(key.lower()):
                            obceOfName.append(obecID)
                return obceOfName

            return KeyError
        raise KeyError
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._data[key]
        elif isinstance(key,str):
            return [k for k,v in self._data.items() if self.deDiacriticize(v.lower()) == self.deDiacriticize(key.lower())]
        raise KeyError
    
    @classmethod
    def actualizeFile(cls):
        cls._data = {}
        for kraj in Kraje():
            cls._data[kraj] = cls.readFromServer(kraj)
            
        cls.saveToFile()
        cls._data = {}

Obce.setup()
    




