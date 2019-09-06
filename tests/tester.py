
from utest_kraje import *
from utest_obce import *
from utest_ctvrti import *

class Tester:
    def setup(self, offline=False):
        self.utests = []
        # add tests
        self.utests.append( UTest_Kraje(offline=offline) )
        self.utests.append( UTest_Obce(offline=offline) )
        self.utests.append( UTest_Ctvrti(offline=offline) )
        self.status = True

    def __init__(self, offline=False):
        self.setup(offline)
    
    def run(self):
        for utest in self.utests:
            utest.run()
            if utest.status is False:
                self.status = False
    
    def check(self):
        try:
            assert(self.status)
        except:
            raise RuntimeError


if __name__ == "__main__":
    tester = Tester(offline=False)
    tester.run()


