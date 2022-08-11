from .Reference import ReferenceSet
import json

class MitigationSet(object):
    
    def __init__(self):
        self.mitigations_by_mid = {}
        self.mitigations_by_uid = {}
        self.mitigates_by_mid = {}
        self.mitigates_by_uid = {}

    def add_mitigation(self, mitigation):
        mid = mitigation.get_mid()
        self.mitigations_by_mid[mid] = mitigation
        uid = mitigation.get_uid()
        self.mitigations_by_uid[uid] = mitigation
        
    def get_mitigation_by_mid(self, mid):
        if mid in self.mitigations_by_mid:
            return self.mitigations_by_mid[mid]
        else:
            raise Exception("Mitigation %s does not exist" % mid)

    def get_mitigation_by_uid(self, uid):
        if uid in self.mitigations_by_uid:
            return self.mitigations_by_uid[uid]
        else:
            raise Exception("Mitigation %s does not exist" % uid)
        
    def get_mitigations_by_uid(self):
        return self.mitigations_by_uid
        
    def get_mitigation_count(self):
        return len(self.mitigations_by_mid)

    def link_technique_to_mitigation(self, mitigation_uid, technique):
        if mitigation_uid in self.mitigates_by_uid:
            self.mitigates_by_uid[mitigation_uid].append(technique)
        else:
            self.mitigates_by_uid[mitigation_uid] = [technique]
        mitigation = self.get_mitigation_by_uid(mitigation_uid)
        mitigation.add_technique(technique)
        mitigation_mid = mitigation.get_mid()
        if mitigation_mid in self.mitigates_by_mid:
            self.mitigates_by_mid[mitigation_mid].append(technique)
        else:
            self.mitigates_by_mid[mitigation_mid] = [technique]


class Mitigation(object):

    def __init__(self, obj):
        self.references = ReferenceSet()
        self.mitigates_by_uid = []
        self.mitigates_by_tid = []
        if "id" in obj:
            self.uid = obj["id"]
        else:
            errmsg = "No id found!\n" + json.dumps(obj, indent=4)
            raise Exception(errmsg)
        if "name" in obj:
            self.name = obj["name"]
        else:
            errmsg = "No name found!\n" + json.dumps(obj, indent=4)
            raise Exception(errmsg)
        if "description" in obj:
            self.description = obj["description"]
        else:
            errmsg = "No description found!\n" + json.dumps(obj, indent=4)
            raise Exception(errmsg)
        if "external_references" in obj:
            for ref in obj["external_references"]:
                if "external_id" in ref and "url" in ref:
                    self.mid = ref["external_id"]
                    self.url = ref["url"]
                elif "url" in ref and "description" in ref and "source_name" in ref:
                    url = ref["url"]
                    description = ref["description"]
                    name = ref["source_name"]
                    self.references.add_reference(name, description, url)
                else:
                    pass

    def is_mitigant(self):
        return True

    def get_uid(self):
        return self.uid

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_mid(self):
        return self.mid

    def get_url(self):
        return self.url
    
    def add_technique(self, technique):
        self.mitigates_by_uid.append(technique.get_uid())
        self.mitigates_by_tid.append(technique.get_tid())
