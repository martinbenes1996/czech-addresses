
import json 

from data.parser import *
from data.kraje import *

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
    def readFromFile(cls, kraj=None):
        with open('data/obce.json','r') as f:
            data = cls.parseIntKeys( json.load(f) )
            if kraj is None:
                cls._data = data
                return cls._data
            else:
                try:
                    assert(int(kraj) in data) # test if index
                except:
                    kraj = Kraje.get(kraj) # convert name to int
                finally:
                    cls._data[int(kraj)]= data[int(kraj)] # update
                    return cls._data[int(kraj)] # return

    @classmethod
    def saveToFile(cls, output="data/obce.json"):
        super().saveToFile(output)
    @classmethod
    def setup(cls):
        try:
            cls.readFromFile()
        except:
            cls.readFromServer()
            cls.saveToFile()
    
    @classmethod
    def get(cls, obec=None, kraj=None):

        # listing
        if obec is None:
            if kraj is None: # !obec & !kraj
                return cls._data
            else: # !obec & kraj
                return cls._data[Kraje.id(kraj)]
        # searching
        else:
            domains = Kraje.get()
            if kraj is not None: # obec & kraj
                domains = [Kraje.id(kraj)]
            print("domains", domains, "because kraj is", kraj)
            print("obec is",obec)

            if isinstance(obec,str) or isinstance(obec,int):
                try:
                    obec = int(obec)
                except: # obecName
                    result = []
                    for d in domains: # forall kraje (domains)
                        for k,v in cls._data[d].items():
                            if cls.deDiacriticize(v.lower()) == cls.deDiacriticize(obec.lower()):
                                result.append(k)
                    if len(result) > 0:
                        return result
                else: # obecId
                    for d in domains: # forall kraje (domains)
                        try:
                            return cls._data[d][obec]
                        except KeyError:
                            pass
                finally:
                    raise KeyError

            raise TypeError

    def __getitem__(self, obec):
        if isinstance(obec, int):
            return self._data[obec]
        elif isinstance(obec,str):
            return [k for k,v in self._data.items() if self.deDiacriticize(v.lower()) == self.deDiacriticize(obec.lower())]
        raise KeyError
    
    @classmethod
    def actualizeFile(cls):
        cls._data = {}
        for kraj in Kraje():
            cls._data[kraj] = cls.readFromServer(kraj)
            
        cls.saveToFile()
        cls._data = {}

Obce.setup()

