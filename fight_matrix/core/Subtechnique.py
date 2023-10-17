import re
from .Technique import Technique

tid_re = re.compile("(T\d\d\d\d).(\d\d\d)")

class Subtechnique(Technique):

    def __init__(self, tid, json_id, tname):
        super().__init__(tid, json_id, tname)
        tid_m = tid_re.match(self.tid)
        if tid_m:
            self.ptid = tid_m.groups()[0]
            self.stid = tid_m.groups()[1]
        self.subtechnique = True