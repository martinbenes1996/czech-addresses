
import sys

class UTest:
    _errors = []
    _kraje = ["Hlavn\u00ed m\u011bsto Praha", "Jiho\u010desk\u00fd", "Jihomoravsk\u00fd",
         "Karlovarsk\u00fd", "Kr\u00e1lov\u00e9hradeck\u00fd", "Libereck\u00fd",
         "Moravskoslezsk\u00fd", "Olomouck\u00fd", "Pardubick\u00fd", 
         "Plze\u0148sk\u00fd", "St\u0159edo\u010desk\u00fd", "\u00dasteck\u00fd",
         "Vyso\u010dina", "Zl\u00ednsk\u00fd"]

    def __del__(self):
        self.listErrorMessages()
    def __init__(self, offline=False):
        self.status = True
        self.offline = offline

    @classmethod
    def perform(cls, name, procedure):
        print("Testing", name+":",end=' ')
        sys.stdout.flush()
        try:
            procedure()
        except Exception as e:
            print('FAIL')
            cls._errors.append( (name, str(e)) )
            raise
        else:
            print('SUCCESS')
    
    @classmethod
    def listErrorMessages(cls):
        if len(cls._errors) > 0:
            self.status = False
            print("Error list:")
        for e in cls._errors:
            print(e)
