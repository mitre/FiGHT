#!/usr/bin/env python3
"""

NOTICE
This software was produced for the U. S. Government under Basic Contract No. W56KGU-18-D-0004, and
is subject to the Rights in Noncommercial Computer Software and Noncommercial Computer Software 
Documentation Clause 252.227-7014 (FEB 2012). Copyright (c) 2022 The MITRE Corporation.

This copyright notice must not be removed from this software, 
absent MITRE's express written permission.

"""
import pprint
import core.parse_json2 as parse_json2
import traceback
import os.path
from core.fight2 import PropositionFactory, ProposedTechnique, ProposedSubtechnique,types
import re
import yaml
import sys
import csv
from word_importer import get_drafts, dump_tables
import logging

pp = pprint.PrettyPrinter(indent=4)
only_whitespace_re = re.compile("^\s+$")

tactics_ordered = [
    "reconnaissance",
    "resource-development",
    "initial-access",
    "execution",
    "persistence",
    "privilege-escalation",
    "defense-evasion",
    "credential-access",
    "discovery",
    "lateral-movement",
    "collection",
    "command-and-control",
    "exfiltration",
    "impact",
    "fraud"
]

tactics_dict = [
          {
              "id": "TA0043",
              "name": "Reconnaissance",
              "myname": "reconnaissance",
              "description": "The adversary is trying to gather information they can use to plan future operations.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0043/) ",
              "object-type": "tactic"
          },
          {
              "id": "TA0042",
              "name": "Resource Development",
              "myname": "resource-development",
              "description": "The adversary is trying to establish resources they can use to support operations.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0042/) ",
              "object-type": "tactic"
          },
          {
              "id": "TA0001",
              "name": "Initial Access",
              "myname": "initial-access",
              "description": "The adversary is trying to get into your network.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0001/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0002",
              "name": "Execution",
              "myname": "execution",
              "description": "The adversary is trying to run malicious code.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0002/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0003",
              "name": "Persistence",
              "myname": "persistence",
              "description": "The adversary is trying to maintain their foothold.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0003/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0004",
              "name": "Privilege Escalation",
              "myname": "privilege-escalation",
              "description": "The adversary is trying to gain higher - level permissions.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0004/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0005",
              "name": "Defense Evasion",
              "myname": "defense-evasion",
              "description": "The adversary is trying to avoid being detected.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0005/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0006",
              "name": "Credential Access",
              "myname": "credential-access",
              "description": "The adversary is trying to steal account names and passwords.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0006/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0007",
              "name": "Discovery",
              "myname": "discovery",
              "description": "The adversary is trying to figure out your environment.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0007/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0008",
              "name": "Lateral Movement",
              "myname": "lateral-movement",
              "description": "The adversary is trying to move through your environment.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0008/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0009",
              "name": "Collection",
              "myname": "collection",
              "description": "The adversary is trying to gather data of interest to their goal.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0009/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0011",
              "name": "Command and Control",
              "myname": "command-and-control",
              "description": "The adversary is trying to communicate with compromised systems to control them.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0011/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0010",
              "name": "Exfiltration",
              "myname": "exfiltration",
              "description": "The adversary is trying to steal data.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0010/)",
              "object-type": "tactic"
          },
          {
              "id": "TA0040",
              "name": "Impact",
              "myname": "impact",
              "description": "The adversary is trying to manipulate, interrupt, or destroy your systems and data.\r\n[View Here at MITRE ATT&CK](https://attack.mitre.org/tactics/TA0040/)",
               "object-type": "tactic"
          },
          {
              "id": "TA5001",
              "name": "Fraud",
              "myname": "fraud",
              "description": "The adversary is trying to obtain service without contractually paying for it",
              "object-type": "tactic"
          }
]

fight_types = [
    "fight_technique",                          #0
    "fight_subtechnique",                       #1
    "fight_subtechnique_to_attack_technique",   #2
    "attack_technique_addendum",                #3
    "attack_subtechnique_addendum",             #4
    "attack_technique_with_subs_with_addendums",#5
    "attack_technique_with_fight_subs",         #6
    "invalid_type"                              #7
]

fight_url = "http://10.128.7.50/v10/techniques"

# ATT&CK Technique TID
tid_re = re.compile("(^T\d\d\d\d)")
# ATT&CK subTechnique TID
stid_re = re.compile("(^T\d\d\d\d).(\d\d\d)")



subtechlabels = [
    "##### This is a FiGHT Technique\r\n",  # 0
    "##### This is a FiGHT Subtechnique\r\n",  # 1
    "##### This is a FiGHT Subtechnique for an ATT&CK Technique\r\n",  # 2
    "##### This is an ATT&CK Technique that has 5G special context, captured in one or more FiGHT Addendums\r\n",  # 3
    "##### This is an ATT&CK Sub Technique that has 5G special context, captured in one or more FiGHT Addendums\r\n",  # 4
    "# This is an invalid type.  You should never see this.  Something has gone horribly wrong.\r\n"
]

html_template = """
<html>
\t<head>
\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"> </script>
\t\t<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css">
\t\t<script type="text/javascript">
\t\t\tfunction showHideRow(row) {
\t\t\t\t$("#" + row).toggle();
\t\t\t}
\t\t</script>
\t\t<link rel="stylesheet" href="table4.css">
\t</head>
\t<body>
\t<H1>The FIGHT Framework</H1>
\t<H2>A 5G Threat Model</H2>
\t<p>First rule about FIGHT Framework:  Don't talk about FIGHT Framework.
\t<p>FIGHT Matrix beta version 0.0.1 
\t<ul>
\t<li>be advised hyperlinks are not yet valid
\t<li>to expand subtechniques, click on the box outside of the text.  Do <b>not</b> click on the hyperlink text
\t</ul>
\t<H3>Legend:</H3>
\t<table>
\t<tr>
\t\t <td style=\"background-color:#7A9AE6; color:#FFFFFF\">Addendum to existing ATT&CK Technique / Subtechnique</td>
\t</tr><tr>
\t\t <td style=\"background-color:#AA3333; color:#FFFFFF\">New FIGHT Technique / Subtechnique</td>
\t</tr><tr>
\t\t <td style=\"background-color:#E67A7A; color:#FFFFFF\">New FIGHT Subtechnique for an existing ATT&CK Technique</td>
\t</tr><tr>
\t<div class="table_div">
\t\t<table>
\t\t\t<thead>
\t\t\t\t<tr>
%s  
\r\r\r\r</tr>
\t\t\t</thead>
\t\t\t<tbody>
\t\t\t\t<tr>
%s                
\t\t\t\t</tr>
\t\t\t</tbody>
\t\t</table>
\t</div>
</body>
</html>
"""

# Takes: completed string of appended technique_cell_templates
tactic_column_template = """
\t\t\t\t\t<td class="tactic">
\t\t\t\t\t\t<table class="techniques-table">
\t\t\t\t\t\t\t<tbody>
%s
\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t</table>
\t\t\t\t\t</td>
"""

# This takes, in order:
# - Technique HTML id (Make TID)
# - technique template color value (consulte table4.css)
# - ATT&CK or FIGHT HREF?
# - technique TID
# - Technique Name
# - Technique HTML id (Make TID)
# - subtechnique cells (already assembled)
technique_cell_template = """
\t\t\t\t\t\t\t\t<tr class="technique-row">
\t\t\t\t\t\t\t\t\t<td onclick="showHideRow('%s');">
\t\t\t\t\t\t\t\t\t\t<table class="supertechnique">
\t\t\t\t\t\t\t\t\t\t\t<tbody>
\t\t\t\t\t\t\t\t\t\t\t\t<tr>
\t\t\t\t\t\t\t\t\t\t\t\t\t<td class="technique">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div class="%s">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a href="%s/%s">%s</a>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t</td>
\t\t\t\t\t\t\t\t\t\t\t\t</tr>
\t\t\t\t\t\t\t\t\t\t\t</tbody>
\t\t\t\t\t\t\t\t\t\t</table>
\t\t\t\t\t\t\t\t\t</td>
\t\t\t\t\t\t\t\t\t<td class="subtechniques-td" id="%s">
\t\t\t\t\t\t\t\t\t\t<div class="subtechniques-container">
%s
\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t</td>
\t\t\t\t\t\t\t\t</tr>
"""

# This takes, in order:
# - technique template color value (consulte table4.css)
# - ATT&CK or FIGHT URL?
# - technique TID
# - subtechnique count
# - Subtechnique Name
# Itterate to produce as many as needed for the Technique cell
subtechnique_cell_template = """
\t\t\t\t\t\t\t\t\t\t\t<div class="subtechnique">
\t\t\t\t\t\t\t\t\t\t\t\t<div class="%s">
\t\t\t\t\t\t\t\t\t\t\t\t\t<a href="%s/%s/%s">%s</a>
\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t</div>
"""

attack_tid_re = re.compile("(T\d\d\d\d)")
attack_stid_re = re.compile("(T\d\d\d\d).(\d\d\d)")
ref_num_re = re.compile("\[(\d+)\]")
ref_re = re.compile("(\[\d+\])")

def link_refs(text):
    return text
    p = r'\[(\d+)\]'
    #r = r'<a href="#\1">\[\1\]</a>'
    r = r'[\[\1\]](#\1)'
    newtext = re.sub(p, r, text)
    return newtext
            

def log_traceback(ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    #tb_lines = [ line.rstrip('\n') for line in
    #             traceback.format_exception(ex.__class__, ex, ex_traceback)]
    tb_lines = "\n".join(traceback.format_exception(ex.__class__, ex, ex_traceback))
    logging.warning(tb_lines)

def get_tactics(attack):
    tactics = []
    for tid in attack:
        technique = attack[tid]
        attack_tid_tactics = technique.get_tactics()
        for tactic in attack_tid_tactics:
            if tactic not in tactics:
                tactics.append(tactic)
    return tactics

def get_gold_csv(filename, enterprise_filename, mobile_filename, drafts=None):
    proposed = {}
    rows = []
    # Get the data from the file
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            rows.append(row)
    # Sanity check things
    tid_list = {}
    failed = False
    index = 0
    logging.info("Processing %s" % enterprise_filename)
    techniques, mitigations = parse_json2.proc_attack_json_tid(enterprise_filename)
    enterprise_attack = [techniques, mitigations]
    logging.info("Processing %s" % mobile_filename)
    techniques, mitigations = parse_json2.proc_attack_json_tid(mobile_filename)
    mobile_attack = [techniques, mitigations]
    prop_factory_obj = PropositionFactory(enterprise_filename, mobile_filename)
    for row in rows:
        tid = row[4].rstrip().lstrip()
        if tid in tid_list:
            other_index = tid_list[tid]
            logging.info(f"WARNING line {index}:  Duplicate TID found:  {tid} in both rows {index} and {other_index}")
        else:
            tid_list[tid] = index
        if not failed:
            index += 1
    if failed:
        sys.exit()
    index = 1
    for row in rows:
        tempid = row[0]
        # ALL ARE BELONG TO 5G!
        domain = row[1]
        # Supplied by the DOCX sources, that is authoritative
        architectures = row[2]
        tactics = row[3].lower()
        temp_tid = row[4]
        t_name = row[5]
        logging.info(f"Processing {temp_tid} {t_name}")
        bluf = row[6]
        source = row[7]
        #print("Processing %s %s %s [%s]" %  (tempid, temp_tid, t_name, tactics))
        try:
            proposal = prop_factory_obj.make_proposition(tempid, temp_tid, t_name)
            if architectures:
                for arch in architectures.split(","):
                    proposal.add_architecture(arch)
        except Exception as err:
            #logging.warning(f"Problem on line {index}: {err}", stack_info=True)
            #log_traceback(err)
            logging.warning(f"Problem on line {index}: {err}")
            proposal = None
        if not proposal:
            continue
        proposal.set_bluf(bluf)
        tid = proposal.get_tid()
        # Check to see if the TID is in Enterprise ATT&CK already
        for tactic in tactics.split(","):
            clean_tactic = tactic.lower().rstrip().lstrip().replace(" ", "-")
            proposal.add_tactic(clean_tactic)
        proposal.add_source(source)
        proposed[tid] = proposal
        index += 1
    # Link up subtechniques to techniques
    new_proposeds = {}
    # pylint: disable=consider-using-dict-items
    for tid in proposed:
        proposal = proposed[tid]
        this_type = proposal.get_type()
        logging.debug("Processing %s:%s for subtechniques" % (tid,proposal.get_name()))
        if this_type == types[3]:
            print(tid)
            original_mobile_attack = mobile_attack[0].get_technique_by_tid(tid)
            original_ent_attack = enterprise_attack[0].get_technique_by_tid(tid)
            if original_mobile_attack:
                proposal.set_bluf(original_mobile_attack.get_bluf())
            elif original_ent_attack:
                proposal.set_bluf(original_ent_attack.get_bluf())
            else:
                raise Exception(f"No (sub)Technique found for {tid}")
        if "subtechnique" in this_type:
            technique_tid = proposal.get_technique_tid()
            logging.debug("Found sub %s for %s" %  (tid, technique_tid))
            if technique_tid in proposed:
                technique = proposed[technique_tid]
                technique.add_subtechnique(proposal)
            if this_type == types[2] or this_type == types[4]:
                if this_type == types[4]:
                    original_attack = enterprise_attack[0].get_technique_by_tid(tid)
                    attack_name = original_attack.get_name()
                    proposed[tid].set_name(attack_name)
                    proposed[tid].set_bluf(original_attack.get_bluf())
                elif this_type == types[2]:
                    attack_tid = proposal.get_technique_tid()
                    original_attack = enterprise_attack[0].get_technique_by_tid(attack_tid)
                    if original_attack:
                        attack_name = original_attack.get_name()
                    else:
                        original_attack = mobile_attack[0].get_technique_by_tid(attack_tid)
                        attack_name = original_attack.get_name()
                    current_name = proposal.get_name()
                    fight_name = f"{attack_name}:{current_name}"
                    proposed[tid].set_name(fight_name)
                attack_technique_tid = proposal.get_technique_tid()
                if attack_technique_tid in proposed:
                    new_proposal = proposed[attack_technique_tid]
                    proposal_tactics = proposal.get_tactics()
                    for tactic in proposal_tactics:
                        new_proposal.add_tactic(tactic)
                elif attack_technique_tid in new_proposeds:
                    proposal_tactics = proposal.get_tactics()
                    for tactic in proposal_tactics:
                        new_proposeds[attack_technique_tid].add_tactic(tactic)
                else:
                    # Pulling in the ATT&CK Technique that has a subTechnique with addendums
                    enterprise_technique = enterprise_attack[0].get_technique_by_tid(attack_technique_tid)
                    mobile_technique = mobile_attack[0].get_technique_by_tid(attack_technique_tid)
                    if enterprise_technique:
                        attack_technique = enterprise_technique
                    elif mobile_technique:
                        attack_technique = mobile_technique
                    else:
                        raise Exception("Unknown ATT&CK TID %s" % attack_technique_tid)
                    attack_name = attack_technique.get_name()
                    logging.info("Adding FiGHT sub %s:%s to %s:%s" % (tid, proposal.get_name(),
                                                               attack_technique_tid, attack_name))
                    new_proposal = ProposedTechnique("Null", attack_technique_tid, attack_name)
                    if this_type == fight_types[2]:
                        new_proposal.set_type(6)
                    elif this_type == fight_types[4]:
                        new_proposal.set_type(5)
                    else:
                        logging.warning(f"TID {tid}: Got unexpected type {this_type} when evaluating ATT&CK Technique {attack_technique_tid}")
                    new_proposal.set_attack(attack_technique)
                    new_proposal.add_subtechnique(proposal)
                    new_proposal.set_bluf(attack_technique.get_bluf())
                    proposal_tactics = proposal.get_tactics()
                    for tactic in proposal_tactics:
                        new_proposal.add_tactic(tactic)
                    new_proposeds[attack_technique_tid] = new_proposal
    for tid in new_proposeds:
        #print("Adding %s to the proposed list" % tid)
        proposed[tid] = new_proposeds[tid]
    return proposed

def get_matrix_by_tactic(proposed):
    matrix = []
    column = 0
    max_row = 0
    for tactic in tactics_ordered:
        # We build by row to write the matrix
        matrix.append([tactic])
        this_len = 0
        for tid in proposed:
            proposal = proposed[tid]
            if "subtechnique" in proposal.get_type():
                continue
            elif proposal.has_tactic(tactic):
                matrix[column].append(proposal)
                this_len += 1
                if this_len > max_row:
                    max_row = this_len
        column += 1
    max_col = column
    return matrix, max_row, max_col

def build_url(tid):
    attack_tid_re_m = attack_tid_re.search(tid)
    attack_stid_re_m = attack_stid_re.search(tid)
    if attack_tid_re_m:
        tid = attack_tid_re_m.groups()[0]
        attack_url = "https://attack.mitre.org/techniques/%s" % tid
        return attack_url
    elif attack_stid_re_m:
        tid = attack_stid_re_m.groups()[0]
        stid = attack_stid_re_m.groups()[1]
        attack_url = "https://attack.mitre.org/techniques/%s/%s" % (tid, stid)
        return attack_url
    else:
        return ""

def write_html_matrix_dynamic(csv_filename, matrix, max_row, max_col, base_indent=0, indent="\t"):
    table_contents = ""
    numi = base_indent
    theaders = ""
    numi += 4
    for col in range(max_col):
        if col < max_col:
            pass
        else:
            break
        theaders += "%s<th>%s</th>\n" % (numi * indent, matrix[col][0])
    for col in range(max_col):
        this_row = ""
        if col < max_col:
            pass
        else:
            break
        tactic = matrix[col][0]
        for row in range(max_row):
            if row == 0:
                continue
            elif row < len(matrix[col]):
                proposal = matrix[col][row]
                tid = proposal.get_tid()
                tname = proposal.get_name()
                proposal_type = proposal.get_type()
                subtechniques = proposal.get_subtechniques()
                subtechniques_html = ""
                subcount = 0
                for stid in subtechniques:
                    subcount += 1
                    subtechnique = subtechniques[stid]
                    ptid = subtechnique.get_technique_tid()
                    stid = subtechnique.get_subtechnique_id()
                    st_name = subtechnique.get_name()
                    sub_type = subtechnique.get_type()
                    if sub_type == types[1]:
                        subtechniques_html += subtechnique_cell_template % ("technique-cell-new-fight", fight_url, ptid, stid, st_name)
                    elif sub_type == types[2]:
                        subtechniques_html += subtechnique_cell_template % ("technique-cell-new-child", fight_url, ptid, stid, st_name)
                    elif sub_type == types[4]:
                        subtechniques_html += subtechnique_cell_template % ("technique-cell-addendum", fight_url, ptid, stid, st_name)
                tname += " (%s)" % subcount
                sub_html_id = "%s-%s" % (tid, tactic)
                if proposal_type == types[0]:
                    technique_html = technique_cell_template % (sub_html_id, "technique-cell-new-fight", fight_url, tid, tname, sub_html_id, subtechniques_html)
                elif proposal_type == types[3]:
                    technique_html = technique_cell_template % (sub_html_id, "technique-cell-addendum", fight_url, tid, tname, sub_html_id, subtechniques_html)
                this_row += technique_html
        table_contents += tactic_column_template % this_row
    html = html_template % (theaders, table_contents)
    matrix_outfilename = "%s.matrix.html" % csv_filename
    matrix_file = open(matrix_outfilename, "w")
    matrix_file.write(html)

def convert_fgtids(tid):
    tid_m = tid_re.match(tid)
    stid_m = stid_re.match(tid)
    if stid_m:
        return "FG"+".".join(stid_m.groups()[0:2])
    elif tid_m:
        return "FG"+tid_m.groups()[0]
    else:
        return tid

def write_yaml(fight, drafts, mitigations=None, datasources=None):
    techniques = []
    def get_taids_array(tactics):
        taids = []
        for tactic in tactics:
            for tactic_dict in tactics_dict:
                if tactic_dict["myname"] == tactic:
                    taids.append(tactic_dict["id"])
        return taids
    for tid in fight:
        fight_name = fight[tid].get_name()
        fight_type_num = fight[tid].get_type_num()
        bluf = fight[tid].get_bluf()
        description = ""
        platforms = []
        critical_assets = []
        proc_examples = []
        pre_conditions = []
        post_conditions = []
        references = []
        addendums = []
        architectures = []
        access_requireds = []
        mitigates_technique = []
        detects_technique = []
        if tid in drafts:
            num_drafts = len(drafts[tid])
            all_platforms = ""
            addendum_header = ""
            for draft in drafts[tid]:
                draft_type = draft.get_type()
                draft_name = draft.get_name()
                logging.info(f"Preparing {tid} {draft_name} ({draft_type}) for YAML output")
                for platform in draft.get_platforms():
                    platforms.append(platform.rstrip().lstrip())
                #for archset in draft.get_architecture():
                for archset in fight[tid].get_architectures():
                    if archset in architectures:
                        continue
                    else:
                        architectures.append(archset)
                for access in draft.get_access_type_req():
                    access_requireds.append(access.rstrip().lstrip())
                platforms_str = ", ".join(draft.get_platforms())
                architectures_str = ", ".join(architectures)
                critical_assets += draft.get_critical_assets_dict()
                status = draft.get_class_md()
                if draft_type == fight_types[3] or draft_type == fight_types[4]:
                    tid_url = tid.replace(".", "/")
                    description = f"{bluf}\r\n[To read more, please see the MITRE ATT&CK page for this technique](https://attack.mitre.org/techniques/{tid_url})\r\n"

                    addendum_name = draft.get_name()
                    desc = link_refs(draft.get_description())
                    addendums.append(f"#### Addendum Name: {addendum_name}\r\n##### Architecture Segments: {architectures_str}\r\n{desc}")
                    proc_examples += draft.get_procedure_examples_dict()
                    pre_conditions += draft.get_pre_conditions_dict()
                    post_conditions += draft.get_post_conditions_dict()
                    references += draft.get_references_dict()
                else:
                    if num_drafts > 1:
                        logging.warning(f"CAUTION!  MULTIPLE DRAFTS FOUND FOR TID {tid} - {fight_name} | {draft_name}.docx")
                    description =  link_refs(draft.get_description())
                    proc_examples += draft.get_procedure_examples_dict()
                    pre_conditions += draft.get_pre_conditions_dict()
                    post_conditions += draft.get_post_conditions_dict()
                    platforms_str += ", ".join(draft.get_platforms())
                    references += draft.get_references_dict()
                #description += "---\r\n\r\n"
                if mitigations:
                    for fgmid in mitigations:
                        these_mitigations = draft.get_mitigations()
                        if fgmid in these_mitigations:
                            if tid not in mitigations[fgmid]["techniques"]:
                                mitigations[fgmid]["techniques"].append(convert_fgtids(tid))
                                mitigates_technique.append({"fgmid": fgmid, "name": mitigations[fgmid]["name"], "mitigates": these_mitigations[fgmid]})
                if datasources:
                    for fgdsid in datasources:
                        these_detections = draft.get_detections()
                        if fgdsid in these_detections:
                            if tid not in datasources[fgdsid]["techniques"]:
                                datasources[fgdsid]["techniques"].append(convert_fgtids(tid))
                                detects_technique.append({"fgdsid": fgdsid, "name": datasources[fgdsid]["name"], "detects": these_detections[fgdsid]})

            #number = 1
            #if len(refs):
            #    for reference in refs:
            #        text = reference[0]
            #        url = reference[1]
            #        link = f"[{text}]({url})"
            #        references += f"##### {number} {link}\r\n"
            #        number += 1
            #label = subtechlabels[fight_type_num]
            #description = "\r\n".join([addendum_header, label, description])
        else:
            tid_url = tid.replace(".", "/")
            description = f"{bluf}\r\n[To read more, please see the MITRE ATT&CK page for this technique](https://attack.mitre.org/techniques/{tid_url})\r\n"
            all_platforms = [f""]
        parent_tid = fight[tid].get_technique_tid()
        if platforms:
            all_platforms_str = ", ".join(platforms)
            if only_whitespace_re.match(all_platforms_str) or not all_platforms_str:
                all_platforms_str = "5G"
        else:
            all_platforms_str = "5G"
        if architectures:
            all_archsegs_str = ", ".join(architectures)
            if only_whitespace_re.match(all_platforms_str) or not all_archsegs_str:
                all_platforms_str = "5G"
        else:
            all_archsegs_str = "5G"
        print(f"{tid} architectures: {all_archsegs_str}")
        technique = {
            "description": description,
            "id": convert_fgtids(tid),
            "name": fight_name,
            "tactics": get_taids_array(fight[tid].get_tactics()),
            "object-type": "technique",
            "platforms": all_platforms_str,
            "architecture-segment": all_archsegs_str,
            "status": status,
            "typecode": fight_types[fight_type_num],
            "mitigations": mitigates_technique,
            "detections": detects_technique
        }
        if addendums:
            technique["addendums"] = addendums
        if bluf:
            technique["bluf"] = bluf
        if proc_examples:
            technique["procedureexamples"] = proc_examples
        if pre_conditions:
            technique["preconditions"] = pre_conditions
        if post_conditions:
            technique["postconditions"] = post_conditions
        if critical_assets:
            technique["criticalassets"] = critical_assets
        if references:
            technique["references"] = references
        if access_requireds:
            all_access_requireds_str = ", ".join(access_requireds)
            if all_access_requireds_str:
                technique["access-required"] = all_access_requireds_str
        if parent_tid:
            technique["subtechnique-of"] = convert_fgtids(parent_tid)
        else:
            subtechniques = fight[tid].get_subtechniques()
            if subtechniques:
                subtechniques_str = ", ".join(subtechniques)
                #technique["subtechniques"] = subtechniques_str
            else:
                subtechniques_str = ""
        techniques.append(technique)
    for tactic in tactics_dict:
        del tactic["myname"]
    mitigations_array = []
    datasources_array = []
    if mitigations:
        for fgmid in mitigations:
            mitigations_array.append(mitigations[fgmid])
    if datasources:
        for fgdsid in datasources:
            datasources_array.append(datasources[fgdsid])
    data = {'case-studies': [],
            'id': 'FiGHT',
            'name': 'FiGHT Threat Matrix',
            'tactics': tactics_dict,
            'techniques': techniques,
            'mitigations': mitigations_array,
            'data sources': datasources_array}
    output_filename = "fight.yaml"
    yaml_file = open(output_filename, "w")
    yaml.dump(data, yaml_file)

def get_mitigations(mitigation_filename="Mitigations.csv"):
    if not os.path.exists(mitigation_filename):
        raise Exception("No Mitigations file found!")
    rows = []
    # Read the file and build the list
    mitigations = {}
    with open(mitigation_filename) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            rows.append(row)
    rownum = 0
    for row in rows:
        fgmid = row[0]
        if "VOID" in fgmid:
            continue
        elif "FGMID" in fgmid:
            continue
        mname = row[1]
        if "VOID" in mname:
            continue
        mdesc = row[2]
        if fgmid in mitigations:
            logging.warning(f"DUPLICATE FGMID {fgmid} FOUND IN ROW {rownum}, SKIPPING")
        else:
            mitigations[fgmid] = {
                "id": fgmid,
                "name": mname,
                "object-type": "mitigation",
                "description": mdesc,
                "techniques": []
            }
        rownum += 1
    return mitigations

def get_datasources(datasources_filename="Detections.csv"):
    if not os.path.exists(datasources_filename):
        raise Exception("No Mitigations file found!")
    rows = []
    # Read the file and build the list
    datasources = {}
    with open(datasources_filename) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            rows.append(row)
    rownum = 0
    for row in rows:
        fgdsid = row[0]
        if "VOID" in fgdsid:
            continue
        elif "FGDSID" in fgdsid:
            continue
        dsname = row[1]
        if "VOID" in dsname:
            continue
        dsdesc = row[2]
        if fgdsid in datasources:
            logging.warning(f"DUPLICATE FGDID {fgdsid} FOUND IN ROW {rownum}, SKIPPING")
        else:
            datasources[fgdsid] = {
                "id": fgdsid,
                "name": dsname,
                "object-type": "data source",
                "description": dsdesc,
                "techniques": []
            }
        rownum += 1
    return datasources

if __name__ == "__main__":
    usage = """USAGE: 
    ./build_matrix.dynamic.py FIGHT_releases.csv enterprise-attack.json mobile-attack.json templates/ FiGHT_Mitigations_for_human_edits.csv FIGHT_DataSources_for_human_edits.csv [stdout]
    """
    log_format = '%(asctime)s %(levelname)-8s %(message)s'
    if len(sys.argv) == 8:
        if sys.argv[7] == "stdout":
            logging.basicConfig(format=log_format, stream = sys.stdout, level=logging.DEBUG)
        else:
            logging.basicConfig(filename='build_matrix.log', format=log_format, level=logging.DEBUG)
    elif len(sys.argv) == 7:
        logging.basicConfig(filename='build_matrix.log', format=log_format, level=logging.DEBUG)
    else:
        print(usage)
        sys.exit(1)
    fight_csv_filename = sys.argv[1]
    logging.info(f"Started processing {fight_csv_filename}")
    enterprise_filename = sys.argv[2]
    mobile_filename = sys.argv[3]
    directory = sys.argv[4]
    pp = pprint.PrettyPrinter(indent=4)
    if directory:
        drafts = get_drafts(directory)
        dump_tables(drafts)
        fight = get_gold_csv(fight_csv_filename, enterprise_filename, mobile_filename, drafts)
        if len(sys.argv) > 5:
            mitigations_filename = sys.argv[5]
            mitigations = get_mitigations(mitigations_filename)
            if len(sys.argv) > 6:
                datasources_filename = sys.argv[6]
                datasources = get_datasources(datasources_filename)
                write_yaml(fight, drafts, mitigations, datasources)
            else:
                write_yaml(fight, drafts, mitigations)
        else:
            write_yaml(fight, drafts)
    else:
        fight = get_gold_csv(fight_csv_filename, enterprise_filename,mobile_filename, drafts)
        ##############################################
        # OLD CODE TO PRODUCE POC WEB MATRIX
        # Enterprise processing
        matrix, max_row, max_col = get_matrix_by_tactic(proposed)
        write_html_matrix_dynamic("%s.enterprise_dynamic" % fight_csv_filename, matrix, max_row, max_col)
        ##############################################
        # Mobile processing
        #matrix, max_row, max_col = get_matrix_by_tactic(mobile_attack, proposed)
        #write_html_matrix_dynamic("%s.mobile" % fight_csv_filename, matrix, max_row, max_col)
