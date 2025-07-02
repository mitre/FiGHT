"""

NOTICE
This software was produced for the U. S. Government under Basic Contract No. W56KGU-18-D-0004, and
is subject to the Rights in Noncommercial Computer Software and Noncommercial Computer Software 
Documentation Clause 252.227-7014 (FEB 2012). Copyright (c) 2022 The MITRE Corporation.

This copyright notice must not be removed from this software, 
absent MITRE's express written permission.

"""
from .Reference import ReferenceSet
import json
import pprint



class TechniqueSet(object):
    
    def __init__(self):
        self.techniques_by_tid = {}
        self.techniques_by_uid = {}
        self.techniques_to_subs_tid = {}
        self.techniques_to_subs_uid = {}
        self.subtechniques_to_techs_tid = {}
        self.subtechniques_to_techs_uid = {}
        self.mitigated_by_uid = {}
        self.mitigated_by_tid = {}

    def get_technique_by_tid(self, tid):
        if tid in self.techniques_by_tid:
            return self.techniques_by_tid[tid]
        else:
            return None
        
    def add_technique(self, technique):
        tid = technique.get_tid()
        self.techniques_by_tid[tid] = technique
        uid = technique.get_uid()
        self.techniques_by_uid[uid] = technique

    def get_technique_by_tid(self, tid):
        if tid in self.techniques_by_tid:
            return self.techniques_by_tid[tid]
        else:
            return None
        
    def get_technique_by_uid(self, uid):
        if uid in self.techniques_by_uid:
            return self.techniques_by_uid[uid]
        else:
            return None

    def get_technique_count(self):
        return len(self.techniques_by_tid)

    def link_subtechnique_to_technique(self, technique_uid, subtechnique_uid):
        technique = self.get_technique_by_uid(technique_uid)
        subtechnique = self.get_technique_by_uid(subtechnique_uid)
        technique_tid = technique.get_tid()
        subtechnique_tid = subtechnique.get_tid()
        subtechnique.set_technique(technique)
        technique.add_subtechnique(subtechnique)
        if technique_uid in self.techniques_to_subs_uid:
            self.techniques_to_subs_uid[technique_uid].append(subtechnique_uid)
        else:
            self.techniques_to_subs_uid[technique_uid] = [subtechnique_uid]
        if technique_tid in self.techniques_to_subs_tid:
            self.techniques_to_subs_tid[technique_tid].append(subtechnique_tid)
        else:
            self.techniques_to_subs_tid[technique_tid] = [subtechnique_tid]
        if subtechnique_tid in self.subtechniques_to_techs_tid:
            err_msg = "Duplicate Subtechnique relationship: %s" % subtechnique_tid
            err_msg += json.dumps(self.subtechniques_to_techs_tid)
            raise Exception(err_msg)
        else:
            self.subtechniques_to_techs_tid[subtechnique_tid] = technique_tid
        if subtechnique_uid in self.subtechniques_to_techs_uid:
            err_msg = "Duplicate Subtechnique relationship: %s" % subtechnique_uid
            err_msg += json.dumps(self.subtechniques_to_techs_uid)
            raise Exception(err_msg)
        else:
            self.subtechniques_to_techs_uid[subtechnique_uid] = technique_uid
    
    def link_mitigation_to_technique(self, technique_uid, mitigation):
        technique = self.get_technique_by_uid(technique_uid)
        technique.add_mitigation(mitigation)
        mitigation_uid = mitigation.get_uid()
        mitigation_mid = mitigation.get_mid()
        if technique_uid in self.mitigated_by_uid:
            self.mitigated_by_uid[technique_uid].append(mitigation_uid)
        else:
            self.mitigated_by_uid[technique_uid] = [mitigation_uid]
        technique_tid = technique.get_tid()
        if technique_tid in self.mitigated_by_tid:
            self.mitigated_by_tid[technique_tid].append(mitigation_mid)
        else:
            self.mitigated_by_tid[technique_tid] = [mitigation_mid]
        
    def print_mitigations_for_techniques_by_mid(self):
        for tid in self.techniques_by_tid:
            technique = self.get_technique_by_tid(tid)
            name = technique.get_name()
            print("%s:%s has these Mitigations:" % (tid, name))
            for mitigation in technique.get_mitigations():
                mid = mitigation.get_mid()
                name = mitigation.get_name()
                print("\t%s:%s" % (mid, name))
                
    def print_subtechniques(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.techniques_to_subs_tid)
        pp.pprint(self.subtechniques_to_techs_tid)
        for tid in self.techniques_to_subs_tid:
            print("%s:%s" % (tid, self.techniques_to_subs_tid[tid]))
        for tid in self.subtechniques_to_techs_tid:
            print("%s:%s" % (tid, self.subtechniques_to_techs_tid[tid]))


class Technique(object):

    def __init__(self, obj):
        self.references = ReferenceSet()
        self.mitigations = []
        self.mitigated_by_uid = {}
        self.mitigated_by_mid = {}
        self.subtechnique = False
        self.subtechniques_by_tid = {}
        self.subtechniques_by_uid = {}
        if "external_references" in obj:
            for ref in obj["external_references"]:
                if "external_id" in ref and "url" in ref and "source_name" in ref:
                    if "mitre-mobile-attack" in ref["source_name"] or "mitre-attack" in ref["source_name"]:
                        pass
                    else:
                        continue
                    self.url = ref["url"]
                    self.tid = ref["external_id"]
                elif "url" in ref and "description" in ref and "source_name" in ref:
                    url = ref["url"]
                    description = ref["description"]
                    name = ref["source_name"]
                    self.references.add_reference(name, description, url)
                else:
                    pass
        if "name" in obj:
            self.name = obj["name"]
        else:
            errmsg = "No name found!\n" + json.dumps(obj, indent=4)
            raise Exception(errmsg)
        if "id" in obj:
            self.uid = obj["id"]
        else:
            errmsg = "No id found!\n" + json.dumps(obj, indent=4)
            raise Exception(errmsg)
        if "revoked" in obj:
            self.revoked = obj["revoked"]
        else:
            pass
        if "x_mitre_deprecated" in obj:
            self.deprecated = obj["x_mitre_deprecated"]
        else:
            self.deprecated = False
        if "x_mitre_is_subtechnique" in obj:
            self.subtechnique = obj["x_mitre_is_subtechnique"]
        else:
            self.subtechnique = False
        if "kill_chain_phases" in obj:
            self.tactics = []
            for phase in obj["kill_chain_phases"]:
                self.tactics.append(phase["phase_name"])
        if "x_mitre_platforms" in obj:
            self.platforms = obj["x_mitre_platforms"]
        else:
            if self.revoked:
                pass
            else:
                errmsg = "No platforms found!\n" + json.dumps(obj, indent=4)
                raise Exception(errmsg)
        if "description" in obj:
            self.description = obj["description"]
            if self.tid == "T1464":
               self.bluf = "An attacker could jam radio signals (e.g. Wi-Fi, cellular, GPS) to prevent the mobile device from communicating."
            else:
                self.bluf = self.description.split(". ")[0] + "."
        else:
            if self.revoked:
                pass
            else:
                errmsg = "No description found!\n" + json.dumps(obj, indent=4)
                raise Exception(errmsg)
        self.permsreq = []
        self.datasources = []
        self.version = ""
        self.created = ""
        self.modified = ""
        self.domain = ""
        self.detections = []
        self.references = []

    def get_bluf(self):
        return self.bluf

    def set_bluf(self, bluf):
        self.bluf = bluf

    def get_tid(self):
        return self.tid

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
    
    def get_uid(self):
        return self.uid

    def get_tid(self):
        return self.tid

    def is_deprecated(self):
        return self.deprecated

    def get_url(self):
        return self.url

    def is_sub(self):
        return self.subtechnique

    def get_tactics(self):
        return self.tactics

    def has_tactic(self, tactic):
        if tactic in self.tactics:
            return True
        else:
            return False

    def get_platforms(self):
       return self.platforms
    
    def add_subtechnique(self, subtechnique):
        subtechnique_uid = subtechnique.get_uid()
        subtechnique_tid = subtechnique.get_tid()
        if subtechnique_uid in self.subtechniques_by_uid:
            self.subtechniques_by_uid[subtechnique_uid].append(subtechnique) 
        else:
            self.subtechniques_by_uid[subtechnique_uid] = subtechnique
        if subtechnique_tid in self.subtechniques_by_tid:
            self.subtechniques_by_tid[subtechnique_tid].append(subtechnique)
        else:
            self.subtechniques_by_tid[subtechnique_tid] = subtechnique
            
    def add_mitigation(self, mitigation):
        self.mitigations.append(mitigation)
        mid = mitigation.get_mid()
        uid = mitigation.get_uid()
        if mid in self.mitigated_by_mid:
            self.mitigated_by_mid[mid].append(mitigation)
        else:
            self.mitigated_by_mid[mid] = [mitigation]
        if uid in self.mitigated_by_uid:
            self.mitigated_by_uid[uid].append(mitigation)
        else:
            self.mitigated_by_uid[uid] = [mitigation]

    def get_mitigations(self):
        return self.mitigations

    def get_mitigations_by_mid(self):
        return self.mitigated_by_mid
    
    def get_mitigations_by_uid(self):
        return self.mitigated_by_uid
