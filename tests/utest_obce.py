
import json
import random
import sys

import utest

sys.path.insert(0, './data')
from obce import *
from kraje import *

class UTest_Obce(utest.UTest):
    def instantiate(self):
        try:
            self.obce = Obce()
        except:
            self.obce = None
            raise
    def readFromServer_all(self):
        data = self.obce.readFromServer()
        self.checkObceData( data )
    def readFromServer_each(self):
        for krajName in self._kraje:
            krajData = self.obce.readFromServer(krajName)
            krajId = Kraje.get(krajName)
            self.checkObceOfKrajData(krajData, krajId)

    def readFromFile_all(self):
        data = self.obce.readFromFile()
        self.checkObceData( data )
    def readFromFile_each(self):
        for krajName in self._kraje:
            krajData = self.obce.readFromFile(krajName)
            krajId = Kraje.get(krajName)
            self.checkObceOfKrajData(krajData, krajId)
        
    def checkObceData(self, data):
        with open('tests/obce.json','r') as fp:
            refdata = json.load(fp)
            for k in refdata.keys():
                self.checkObceOfKrajData(refdata[k], k)

    def checkObceOfKrajData(self, data, kraj):
        with open('tests/obce.json','r') as fp:
            refdata = json.load(fp)[str(kraj)]
            n = min(10, len(refdata))
            for _ in range(n):
                _,refName = list(refdata.items())[ random.randint(0,len(refdata)-1) ] # random village of reference
                assert(refName in data.values())
    
    def get_all(self):
        data = Obce.get()
        self.checkObceData(data)
    def get_obecName(self):
        for krajName in self._kraje:
            krajId = Kraje.id(krajName)
            data = Obce.get(kraj=krajName)
            self.checkObceOfKrajData(data, krajId)
    def get_obecId(self):
        for krajName in self._kraje:
            krajId = Kraje.id(krajName)
            data = Obce.get(kraj=krajId)
            self.checkObceOfKrajData(data, krajId)

    def search_all(self):
        pass
    def search_kraj(self):
        pass
                
    
    def run(self):
        self.perform("instantitation", self.instantiate)
        self.perform("file reading [whole]", self.readFromFile_all)
        self.perform("file reading [parts]", self.readFromFile_each)
        self.perform("get [whole]", self.get_all)
        self.perform("get [by krajName]", self.get_obecName)
        self.perform("get [by krajId]", self.get_obecId)
        self.perform("search [in all]", self.search_all)
        self.perform("search [in kraj]", self.search_kraj)
        if not self.offline:
            self.perform("API parsing [whole]", self.readFromServer_all)
            self.perform("API parsing [parts]", self.readFromServer_all)
    @classmethod
    def perform(cls, name, procedure):
        super().perform('UTest_Obce '+name, procedure)

if __name__=="__main__":
    utest_obce = UTest_Obce(offline=False)
    utest_obce.run()



