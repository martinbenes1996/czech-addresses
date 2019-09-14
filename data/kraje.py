
import json

from data.parser import *
import parser
print("parser imported successfully")
print(parser)

class Kraje(Parser):
    @classmethod
    def readFromServer(cls):
        cls._data = cls.getOnlineJsonList('https://b2c.cpost.cz/services/Address/getRegionListAsJson', 'seznam kraju')
        return cls._data
    @classmethod
    def readFromFile(cls):
        with open('data/kraje.json','r') as f:
            cls._data = cls.parseIntKeys( json.load(f) )
            return cls._data
    @classmethod
    def saveToFile(cls, output="data/kraje.json"):
        super().saveToFile(output)

    @classmethod
    def get(cls, key=None):
        if key == None:
            return cls._data
        
        elif isinstance(key, str):
            try:
                key = int(key)
            except:
                for k,v in cls._data.items():
                    if cls.deDiacriticize(v.lower()) == cls.deDiacriticize(key.lower()):
                        return k
        
        if isinstance(key, int):
            return cls._data[key]
        
        raise KeyError

    def __getitem__(self, key):
        return self.get(key)  

    @classmethod
    def id(cls, key):
        try:
            key = int(key)
        except:
            return cls.get(key)
        else:
            if key in cls._data.keys():
                return key
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