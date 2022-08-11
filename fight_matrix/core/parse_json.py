import json
from .Technique import Technique
from .Subtechnique import Subtechnique

def proc_attack_json_tid(attack_filename):
    json_file = open(attack_filename)
    json_data = json.load(json_file)
    count = 0
    abridged = {}
    for obj in json_data["objects"]:
        if "type" in obj:
            if obj["type"] == "attack-pattern":
                pass
            else:
                continue
        if "name" in obj:
            t_name = obj["name"]
        if "id" in obj:
            json_id = obj["id"]
        if "x_mitre_deprecated" in obj:
            deprecated = obj["x_mitre_deprecated"]
        else:
            deprecated = None
        if "x_mitre_is_subtechnique" in obj:
            subtechnique = obj["x_mitre_is_subtechnique"]
        else:
            subtechnique = None
        if "kill_chain_phases" in obj:
            tactics = []
            for phase in obj["kill_chain_phases"]:
                tactics.append(phase["phase_name"])
        if "x_mitre_platforms" in obj:
            platforms = obj["x_mitre_platforms"]
        if "external_references" in obj:
            for ref in obj["external_references"]:
                if "external_id" in ref:
                    if ref["source_name"] == "mitre-attack" or ref["source_name"] == "mitre-mobile-attack":
                        tid = ref["external_id"]
                        if subtechnique:
                            this_technique = Subtechnique(tid, json_id, t_name)
                        else:
                            this_technique = Technique(tid, json_id, t_name)
                        if deprecated:
                            this_technique.deprecate()
                        for tactic in tactics:
                            this_technique.add_tactic(tactic)
                        for platform in platforms:
                            this_technique.add_platform(platform)
                        this_technique.set_url(ref["url"])
                        abridged[tid] = this_technique
                        count += 1
    print("Found %s tids" % len(abridged))
    return abridged

