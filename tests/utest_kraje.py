
import json
import random

import utest

from data.kraje import *

class UTest_Kraje(utest.UTest):
    def instantiate(self):
        try:
            self.instance = Kraje()
        except:
            self.instance = None
            raise

    def get_all(self):
        data = Kraje.get()
        self.checkKrajeData(data)
    def get_each(self):
        for kraj in self._kraje:
            data = Kraje.get(kraj)
            assert(kraj == Kraje.get(data))
    def getitem(self):
        for kraj in self._kraje:
            data = self.instance[kraj]
            assert(data == Kraje.get(kraj))
            assert(kraj == Kraje.get(data))

    def readFromServer(self):
        data = Kraje.readFromServer()
        self.checkKrajeData(data)
    
    def readFromFile(self):
        data = Kraje.readFromFile()
        self.checkKrajeData(data)

    def id(self):
        for kraj in self._kraje:
            i = Kraje.id(kraj)
            assert(kraj == Kraje.get(i))
            assert(i == Kraje.get(kraj))
            assert(i == Kraje.id(i))
    def iterate(self):
        data = {k:Kraje.get(k) for k in Kraje()}
        self.checkKrajeData(data)
    

    def checkKrajeData(self, data):
        assert(len(data) == 14)
        v = set(data.values())
        for kraj in self._kraje:
            assert(kraj in v)
                
    
    def run(self):
        self.perform("instantitation", self.instantiate)
        self.perform("static acquisition [whole]", self.get_all)
        self.perform("static acquisition [parts]", self.get_each)
        self.perform("instantious acquisition", self.getitem)
        self.perform("file reading", self.readFromFile)
        self.perform("id", self.id)
        self.perform("iterator", self.iterate)
        if not self.offline:
            self.perform("API parsing", self.readFromServer)
    @classmethod
    def perform(cls, name, procedure):
        super().perform('UTest_Kraje '+name, procedure)

if __name__=="__main__":
    utest_kraje = UTest_Kraje(offline=True)
    utest_kraje.run()



