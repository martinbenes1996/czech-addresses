
import json
import random
import sys

import utest

sys.path.insert(0, './data')
from ctvrti import *
from obce import *
from kraje import *

class UTest_Ctvrti(utest.UTest):
    def instantiate(self):
        try:
            self.ctvrti = Ctvrti()
        except:
            self.obce = None
            raise
    def readFromServer(self):
        pass
    def readFromFile(self):
        pass
    
    def checkCtvrtiData(self, data):
        pass
    def checkCtvrtiOfObecData(self, data, obec):
        pass
    
    def get_all(self):
        pass
    def get_byObec(self):
        pass
    def get_byPsc(self):
        pass
    def getitem(self):
        pass
    
    def id(self):
        pass
    def iterate(self):
        pass
    
    def run(self):
        self.perform("instantiation", self.instantiate)
        self.perform("static acquisition [whole]", self.get_all)
        self.perform("static acquisition [by obec]", self.get_byObec)
        self.perform("static acquisition [by psc]", self.get_byPsc)
        self.perform("instantious acquisition", self.getitem)
        self.perform("file reading", self.readFromFile)
        self.perform("id", self.id)
        self.perform("iterator", self.iterate)
        if not self.offline:
            self.perform("API parsing", self.readFromServer)
    @classmethod
    def perform(cls, name, procedure):
        super().perform("UTest_Ctvrti "+name, procedure)
