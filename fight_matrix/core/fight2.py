"""

NOTICE
This software was produced for the U. S. Government under Basic Contract No. W56KGU-18-D-0004, and
is subject to the Rights in Noncommercial Computer Software and Noncommercial Computer Software 
Documentation Clause 252.227-7014 (FEB 2012). Copyright (c) 2022 The MITRE Corporation.

This copyright notice must not be removed from this software, 
absent MITRE's express written permission.

"""
import logging

import core.parse_json2 as parse_json2
import re


tid_re = re.compile("(^T\d\d\d\d).(\d\d\d)")
# FIGHT Technique TID
fight_tid_re = re.compile("^(FGT\d\d\d\d)$")
# FIGHT Subtechnique TID
fight_sub_tid_re = re.compile("^(FGT\d\d\d\d\.\d\d\d)$")
fight_sub_tid_re2 = re.compile("^(FGT\d\d\d\d)\.(\d\d\d)$")
# FIGHT Subtechnique added to existing ATT&CK
attack_fight_sub_tid_re = re.compile("(T\d\d\d\d\.5\d\d)")
attack_fight_sub_tid_re2 = re.compile("(T\d\d\d\d)\.(5\d\d)")
# ATT&CK Technique TID
attack_tid_re = re.compile("ADDENDUM TO (T\d\d\d\d)$", re.IGNORECASE)
attack_stid_re = re.compile("ADDENDUM TO (T\d\d\d\d.\d\d\d)", re.IGNORECASE)
# ATT&CK Subtechnique TID
attack_sub_tid_re = re.compile("ADDENDUM TO (T\d\d\d\d\.\d\d\d)", re.IGNORECASE)
attack_sub_tid_re2 = re.compile("ADDENDUM TO (T\d\d\d\d)\.(\d\d\d)", re.IGNORECASE)
types = [
         "fight_technique",                           #0
         "fight_subtechnique",                        #1
         "fight_subtechnique_to_attack_technique",    #2
         "attack_technique_addendum",                 #3
         "attack_subtechnique_addendum",              #4
         "attack_technique_with_subs_with_addendums"  #5
         "attack_technique_with_fight_subs",          #6
         "invalid_type"                               #7
]

arch_lookup = {
   "App Layer": "Application Layer",
   "Arch-App Layer": "Application Layer",
   "Arch-Control plane": "Control Plane",
   "Arch-ICAM": "ICAM",
   "Arch-MEC": "MEC",
   "Arch-OA&M": "OA&M",
   "Arch-RAN": "RAN",
   "Arch-Roaming": "Roaming",
   "Arch-Slice": "Network Slice",
   "Arch-UE": "UE",
   "Arch-User plane": "User Plane",
   "control plane": "Control Plane",
   "Impl-CSP": "Cloud Service Provider",
   "Impl-OA&M": "OA&M",
   "Impl-Virtualization": "Virtualization",
   "PHYS & Env": "Physical & Environmental",
   "RAN": "RAN",
   "Roaming": "Roaming",
   "Supply-Chain": "Supply Chain",
   "UE": "UE",
   "user-plane": "User Plane"
}

class PropositionFactory(object):

    def __init__(self, enterprise_filename, mobile_filename):
        logging.info("Processing %s" % enterprise_filename)
        techniques, mitigations = parse_json2.proc_attack_json_tid(enterprise_filename)
        self.enterprise_attack = [techniques, mitigations]
        logging.info("Processing %s" % mobile_filename)
        techniques, mitigations = parse_json2.proc_attack_json_tid(mobile_filename)
        self.mobile_attack = [techniques, mitigations]

    def make_proposition(self, tempid, temp_tid, t_name):
        fight_tid_m = fight_tid_re.search(temp_tid.lstrip().rstrip())
        fight_sub_tid_m = fight_sub_tid_re.search(temp_tid.lstrip().rstrip())
        attack_fight_sub_tid_m = attack_fight_sub_tid_re.search(temp_tid.lstrip().rstrip())
        attack_sub_tid_m = attack_sub_tid_re.search(temp_tid.lstrip().rstrip())
        attack_tid_m = attack_tid_re.search(temp_tid.lstrip().rstrip())
        if attack_sub_tid_m:  # existing ATT&CK Subtechnique TID?
            tid = attack_sub_tid_m.groups()[0]
            enterprise_technique = self.enterprise_attack[0].get_technique_by_tid(tid)
            mobile_technique = self.mobile_attack[0].get_technique_by_tid(tid)
            if enterprise_technique:
                proposal = ProposedSubtechnique(tempid, tid, t_name)
                proposal.set_attack(enterprise_technique)
                proposal.set_type(4)
                return proposal
            elif mobile_technique:
                proposal = ProposedSubtechnique(tempid, tid, t_name)
                proposal.set_attack(mobile_technique)
                proposal.set_type(4)
                return proposal
            else:
                errmsg = "Cannot find %s (%s:%s) in ATT&CK" % (tid, tempid, t_name)
                raise Exception(errmsg)
        elif attack_tid_m:  # existing ATT&CK Technique TID?)
            tid = attack_tid_m.groups()[0]
            enterprise_technique = self.enterprise_attack[0].get_technique_by_tid(tid)
            mobile_technique = self.mobile_attack[0].get_technique_by_tid(tid)
            if enterprise_technique:
                tname = enterprise_technique.get_name()
                proposal = ProposedTechnique(tempid, tid, t_name)
                proposal.set_attack(enterprise_technique)
                proposal.set_name(tname)
                proposal.set_type(3)
                return proposal
            elif mobile_technique:
                tname = mobile_technique.get_name()
                proposal = ProposedTechnique(tempid, tid, t_name)
                proposal.set_attack(mobile_technique)
                proposal.set_name(tname)
                proposal.set_type(3)
                return proposal
            else:
                errmsg = "Cannot find %s (%s:%s) in ATT&CK" % (tempid, tid, t_name)
                raise Exception(errmsg)
        elif fight_tid_m:  # FIGHT Technique TID?
            tid = fight_tid_m.groups()[0]
            proposal = ProposedTechnique(tempid, tid, t_name)
            proposal.set_type(0)
            return proposal
        elif fight_sub_tid_m:  # FIGHT Subtechnique TID?
            tid = fight_sub_tid_m.groups()[0]
            proposal = ProposedSubtechnique(tempid, tid, t_name)
            proposal.set_type(1)
            return proposal
        elif attack_fight_sub_tid_m:  # FIGHT Subtechnique to ATT&CK Technique?
            tid = attack_fight_sub_tid_m.groups()[0]
            proposal = ProposedSubtechnique(tempid, tid, t_name)
            proposal.set_type(2)
            return proposal
        else:
            raise Exception(f"WARNING!  Skipping unrecognized TID format {temp_tid} for tempID {tempid} named '{t_name}'")

class Proposed(object):

    def __init__(self, tempid, tid, name):
        self.tempid = tempid
        self.tid = tid.lstrip().rstrip()
        self.name = name
        self.tactics = []
        self.bluf = ""
        self.source = []
        self.is_attack = False
        self.platforms = []
        self.sources = []
        self.type = None
        self.type_num = 5
        self.is_technique = False
        self.is_subtechnique = False
        self.architectures = []

    def check_subtechnique(self):
        return self.is_subtechnique

    def check_technique(self):
        return self.is_technique

    def set_type(self, this_type):
        if this_type < len(types):
            self.type = types[this_type]
            self.type_num = this_type
            logging.debug(f"Setting TID {self.tid} to type {self.type} ({this_type})")
        else:
            errmsg = "Improper type value (%s) given for %s" % (this_type,
                               self.tempid+":"+self.tid+":"+self.name)
            raise Exception(errmsg)

    def get_type(self):
        return self.type

    def get_type_num(self):
        return self.type_num

    def set_tempid(self, tempid):
        self.tempid = tempid

    def get_tempid(self):
        return self.tempid

    def get_tid(self):
        return self.tid

    def set_name(self, name):
        if ":" in name:
            fight_name = name.split(":")[-1:][0]
        elif ";" in name:
            fight_name = name.split(";")[-1:][0]
        else:
            fight_name = name
        self.name = fight_name

    def get_name(self):
        return self.name

    def add_tactic(self, tactic):
        if tactic.lower() in self.tactics:
            logging.warning("WARNING:  Proposed %s %s already has %s" % (self.tempid, self.name, tactic))
        else:
            self.tactics.append(tactic.lower())

    def get_tactics(self):
        return self.tactics

    def has_tactic(self, tactic):
        if tactic in self.tactics:
            return True
        else:
            return False

    def add_architecture(self, architecture):
        clean_arch = architecture.lstrip().rstrip()
        if clean_arch in arch_lookup:
            arch_value = arch_lookup[clean_arch]
            if arch_value in self.architectures:
                logging.warning(f"{self.tempid}: {self.name} already has Architecture {arch_value}")
            else:
                self.architectures.append(arch_value)
        else:
            logging.warning(f"{self.tempid}: {self.name} has invalid Architecture value {clean_arch}")

    def get_architectures(self):
        return self.architectures

    def add_platform(self, platform):
        if platform in self.platforms:
            raise Exception("Technique %s %s already has %s" % (self.tempid, self.name, platform))
        else:
            self.platforms.append(platform)

    def get_platforms(self):
        return self.platforms

    def set_bluf(self, text):
        self.bluf = text

    def get_bluf(self):
        return self.bluf

    def add_source(self, source):
        self.source.append(source)

    def get_sources(self):
        return self.sources

    def set_attack(self, technique):
        self.is_attack = True
        self.attack_technique = technique

    def check_attack(self):
        return self.is_attack

    def get_attack(self):
        if self.is_attack:
            return self.attack_technique
        else:
            return None


class ProposedTechnique(Proposed):

    def __init__(self, tempid, tid, name):
        super().__init__(tempid, tid, name)
        self.subtechniques = {}
        self.tempid = tempid
        self.tid = tid
        self.name = name
        self.is_attack = False
        self.source = []
        self.is_technique = True

    def add_subtechnique(self, subtechnique):
        stid = subtechnique.get_tid()
        self.subtechniques[stid] = subtechnique

    def get_subtechnique(self, stid):
        if stid in self.subtechniques:
            return self.subtechniques[stid]
        else:
            return None

    def get_subtechniques(self):
        return self.subtechniques

    def get_technique_tid(self):
        None

class ProposedSubtechnique(Proposed):

    def __init__(self, tempid, tid, name):
        super().__init__(tempid, tid, name)
        tid_m = tid_re.match(self.tid)
        attack_fight_sub_tid_m = attack_fight_sub_tid_re2.match(self.tid)
        fight_sub_tid_m = fight_sub_tid_re2.match(self.tid)
        self.is_subtechnique = True
        self.technique = None
        if fight_sub_tid_m:
            self.ptid = fight_sub_tid_m.groups()[0]
            self.stid = fight_sub_tid_m.groups()[1]
        elif tid_m:
            self.ptid = tid_m.groups()[0]
            self.stid = tid_m.groups()[1]
        elif attack_fight_sub_tid_m:
            self.ptid = attack_fight_sub_tid_m.groups()[0]
            self.stid = attack_fight_sub_tid_m.groups()[1]
        else:
            raise Exception("Invalid Technique ID %s!" % self.tid)
        self.subtechnique = True

    def get_technique_tid(self):
        return self.ptid

    def get_subtechnique_id(self):
        return self.stid

    def set_technique(self, technique):
        self.technique = technique

    def get_technique(self):
        return self.technique
