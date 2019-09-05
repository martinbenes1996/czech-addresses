
import json

from parser import *

class Kraje(Parser):
    @classmethod
    def readFromServer(cls):
        cls._data = cls.getOnlineJsonList('https://b2c.cpost.cz/services/Address/getRegionListAsJson', 'seznam kraju')
        return cls._data
    @classmethod
    def readFromFile(cls):
        with open('data/kraje.json','r') as f:
            cls._data = cls.parseIntKeys( json.load(f) )
    @classmethod
    def saveToFile(cls, output="data/kraje.json"):
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
    def id(cls, key):
        if isinstance(key,int) and key in cls._data.keys():
            return key
        elif isinstance(key,str):
            return cls.get(key)
        raise TypeError
    
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