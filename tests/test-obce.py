
import json
import random
import sys

import test

sys.path.insert(0, './data')
from obce import *
from kraje import *

class ObceUTest(test.Test):
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
        for krajName in self.kraje:
            krajData = self.obce.readFromServer(krajName)
            krajId = Kraje.get(krajName)
            self.checkObceOfKrajData(krajData, krajId)

    def readFromFile_all(self):
        data = self.obce.readFromFile()
        self.checkObceData( data )
    def readFromFile_each(self):
        for krajName in self.kraje:
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
        pass
    def get_byId(self):
        pass
    def get_byName(self):
        pass
                
            


    def __init__(self, offline=False):
        self.offline = offline
    
    def test(self):
        self.perform("instantitation", self.instantiate)
        self.perform("file reading [whole]", self.readFromFile_all)
        self.perform("file reading [parts]", self.readFromFile_each)
        if not self.offline:
            self.perform("API parsing [whole]", self.readFromServer_all)
            self.perform("API parsing [parts]", self.readFromServer_all)
    @classmethod
    def perform(cls, name, procedure):
        super().perform('Obec '+name, procedure)

if __name__=="__main__":
    obcetest = ObceUTest(offline=False)
    obcetest.test()



