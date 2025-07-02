#!/usr/bin/env python3
import pprint
import sys
import csv

from core.spreadsheets import get_gold_csv

def find_dupe_tids(spreadsheet_json):
    all_tids = {}
    for tempid in spreadsheet_json:
        json_obj = spreadsheet_json[tempid]
        tid = spreadsheet_json[tempid]["tid"]
        if tid in all_tids:
            all_tids[tid][tempid] = json_obj
        else:
            all_tids[tid] = {tempid: json_obj}
    #pp = pprint.PrettyPrinter()
    #pp.pprint(all_tids)
    for tid in all_tids:
        print("%s: %s" % (tid, len(all_tids[tid])))
    with open("references_dedupe.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        for tid in all_tids:
            for tempid in all_tids[tid]:
                csv_writer.writerow([tid, tempid, all_tids[tid][tempid]["source"]])

if __name__ == "__main__":
    filename = sys.argv[1]
    spreadsheet_json = get_gold_csv(filename)
    find_dupe_tids(spreadsheet_json)