"""

NOTICE
This software was produced for the U. S. Government under Basic Contract No. W56KGU-18-D-0004, and
is subject to the Rights in Noncommercial Computer Software and Noncommercial Computer Software 
Documentation Clause 252.227-7014 (FEB 2012). Copyright (c) 2022 The MITRE Corporation.

This copyright notice must not be removed from this software, 
absent MITRE's express written permission.

"""
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
        