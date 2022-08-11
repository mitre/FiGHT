import re
from .Technique2 import Technique

tid_re = re.compile("(T\d\d\d\d).(\d\d\d)")

class Subtechnique(Technique):

    def __init__(self, obj):
        super().__init__(obj)
        tid_m = tid_re.match(self.tid)
        self.technique = None
        if tid_m:
            self.ptid = tid_m.groups()[0]
            self.stid = tid_m.groups()[1]
        else:
            raise Exception("Invalid Technique ID %s!" % self.tid)
        self.subtechnique = True

    def get_technique_tid(self):
        return self.ptid
        
    def set_technique(self, technique):
        self.technique = technique
        
    def get_technique(self):
        return self.technique
        