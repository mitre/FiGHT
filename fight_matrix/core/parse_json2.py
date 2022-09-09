#!/usr/bin/env python3
"""

NOTICE
This software was produced for the U. S. Government under Basic Contract No. W56KGU-18-D-0004, and
is subject to the Rights in Noncommercial Computer Software and Noncommercial Computer Software 
Documentation Clause 252.227-7014 (FEB 2012). Copyright (c) 2022 The MITRE Corporation.

This copyright notice must not be removed from this software, 
absent MITRE's express written permission.

"""
import re
import json
from .Technique2 import Technique, TechniqueSet
from .Mitigation import Mitigation, MitigationSet 
from .Subtechnique2 import Subtechnique

mid_re = re.compile("M\d\d\d\d")

def proc_attack_json_tid(attack_filename):
    json_file = open(attack_filename)
    json_data = json.load(json_file)
    techniques = TechniqueSet()
    mitigations = MitigationSet()
    mitigates_by_uid = {}
    mitigated_by_uid = {}
    techniques_to_subs_tid = {}
    for obj in json_data["objects"]:
        if "type" in obj:
            if obj["type"] == "attack-pattern":
                techniques.add_technique(parse_technique(obj))
            elif obj["type"] == "course-of-action":
                coa = parse_coa(obj)
                if coa:
                    if coa.is_mitigant():
                        mitigations.add_mitigation(coa)
            elif obj["type"] == "relationship":
                # Mitigations
                if "relationship_type" in obj and "source_ref" in obj and "target_ref" in obj:
                    if obj["relationship_type"] == "mitigates":
                        mitigation_uid = obj["source_ref"]
                        technique_uid = obj["target_ref"]
                        if mitigation_uid in mitigates_by_uid:
                            mitigates_by_uid[mitigation_uid].append(technique_uid)
                        else:
                            mitigates_by_uid[mitigation_uid] = [technique_uid]
                        if technique_uid in mitigated_by_uid:
                            mitigated_by_uid[technique_uid].append(mitigation_uid)
                        else:
                            mitigated_by_uid[technique_uid] = [mitigation_uid]
                    elif obj["relationship_type"] == "subtechnique-of":
                        subtechnique_uid = obj["source_ref"]
                        technique_uid = obj["target_ref"]
                        if technique_uid in techniques_to_subs_tid:
                            techniques_to_subs_tid[technique_uid].append(subtechnique_uid)
                        else:
                            techniques_to_subs_tid[technique_uid] = [subtechnique_uid]
            else:
                continue
    for mitiation_uid in mitigates_by_uid:
        for technique_uid in mitigates_by_uid[mitiation_uid]:
            technique = techniques.get_technique_by_uid(technique_uid)
            mitigations.link_technique_to_mitigation(mitigation_uid, technique)
    for technique_uid in mitigated_by_uid:
        for mitigation_uid in mitigated_by_uid[technique_uid]:
            try:
                mitigation = mitigations.get_mitigation_by_uid(mitigation_uid)
                techniques.link_mitigation_to_technique(technique_uid, mitigation)
            except:
                pass
    for technique_uid in techniques_to_subs_tid:
        for subtechnique_uid in techniques_to_subs_tid[technique_uid]:
            techniques.link_subtechnique_to_technique(technique_uid, subtechnique_uid)
    print("Found %s tids" % techniques.get_technique_count())
    print("Found %s mitigations" % mitigations.get_mitigation_count())
    return (techniques, mitigations)

def parse_coa(obj):
    if "external_references" in obj:
        for ref in obj["external_references"]:
            if "external_id" in ref:
                #if mid_re.match(ref["external_id"]):
                return Mitigation(obj)
                # else:
                #     return None

def parse_technique(obj):
    if "x_mitre_is_subtechnique" in obj:
        subtechnique = obj["x_mitre_is_subtechnique"]
    else:
        subtechnique = None
    if "external_references" in obj:
        for ref in obj["external_references"]:
            if "external_id" in ref:
                if ref["source_name"] == "mitre-attack" or ref["source_name"] == "mitre-mobile-attack":
                    if subtechnique:
                        this_technique = Subtechnique(obj)
                    else:
                        this_technique = Technique(obj)
    return this_technique

if __name__ == "__main__":
    for attack_filename in ("enterprise-attack.json", "mobile-attack.json"):
        print("Processing %s" % attack_filename)
        techniques, mitigations = proc_attack_json_tid(attack_filename)
        techniques.print_mitigations_for_techniques_by_mid()
        techniques.print_subtechniques()
