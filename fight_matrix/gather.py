#!/usr/bin/env python3
import json
import sys
from core.Technique import Technique
from core.Subtechnique import Subtechnique

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

def write_matrix_md(attack, filename):
    outfile = open("%s.md" % filename, "w")
    outfile.write("|TID|Name|sub?|Tactics|Platforms|\n")
    outfile.write("|---|----|----|-------|---------|\n")
    for tid in sorted(attack.keys()):
        technique = attack[tid]
        tactics_txt = ",".join(technique.get_tactics())
        platforms_txt = ",".join(technique.get_platforms())
        if technique.is_sub():
            outfile.write("|%s|%s|Y|%s|%s|\n" % (technique.get_tid(), technique.get_name(), tactics_txt, platforms_txt))
        else:
            outfile.write("|%s|%s|N|%s|%s|\n" % (technique.get_tid(), technique.get_name(), tactics_txt, platforms_txt))

def write_matrix_by_platform_md(attack, filename):
    all_platforms = []
    for tid in attack:
        technique = attack[tid]
        platforms = technique.get_platforms()
        for platform in platforms:
            if platform in all_platforms:
                pass
            else:
                all_platforms.append(platform)
    for platform in all_platforms:
        outfile = open("%s.%s.md" % (filename, platform), "w")
        outfile.write("|TID|Name|sub?|Tactics|Platforms|\n")
        outfile.write("|---|----|----|-------|---------|\n")
        for tid in sorted(attack.keys()):
            technique = attack[tid]
            if platform in technique.get_platforms():
                tactics_txt = ",".join(technique.get_tactics())
                platforms_txt = ",".join(technique.get_platforms())
                if technique.is_sub():
                    outfile.write("|%s|%s|Y|%s|%s|\n" % (technique.get_tid(), technique.get_name(), tactics_txt, platforms_txt))
                else:
                    outfile.write("|%s|%s|N|%s|%s|\n" % (technique.get_tid(), technique.get_name(), tactics_txt, platforms_txt))


if __name__ == "__main__":
   filename = sys.argv[1]
   attack = proc_attack_json_tid(filename)
   write_matrix_md(attack, filename)
   write_matrix_by_platform_md(attack, filename)
