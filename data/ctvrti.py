


import json

from parser import *
from kraje import *
from obce import *

class Ctvrti(Parser):
    @classmethod
    def readFromServer(cls, obec=None):
        return {}

    @classmethod
    def readFromFile(cls, obec=None):
        return {}

    @classmethod
    def saveToFile(cls, output="data/ctvrti.json"):
        super().saveToFile(output)

    @classmethod
    def setup(cls):
        try:
            cls.readFromFile()
        except:
            cls.readFromServer()
            cls.saveToFile()
    
    @classmethod
    def get(cls, obec=None):
        return None

    def __getitem__(self, obec):
        return None
    
    @classmethod
    def actualizeFile(cls):
        pass

Ctvrti.setup()

