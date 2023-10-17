#!/usr/bin/env python3

import yaml
import pandas as pd
import pprint
from tabulate import tabulate
from argparse import ArgumentParser, Namespace

pp = pprint.PrettyPrinter(indent=4)
debug = False

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-1", "--file1", help="path to YAML file 1 to diff")
    parser.add_argument("-2", "--file2", help="path to YAML file 2 to diff")
    args = parser.parse_args()
    return args 

def read_yaml(filename):
    infile = open(filename)
    fight = yaml.safe_load(infile)
    return fight

def find_fgtid(fight, fgtid):
    if "techniques" in fight:
        for object in fight["techniques"]:
            if object["id"] == fgtid:
                return object
    return False

def diff_str(filename1, filename2, object1, object2, element_name):
    if element_name in object1 and element_name in object2:
        element1 = object1[element_name]
        element2 = object2[element_name]
        if element1 != element2:
            return pd.DataFrame([[element_name, element1, element2]], columns=["element", filename1, filename2])
    return pd.DataFrame([[]])

def diff_list(filename1, filename2, object1, object2, element_name):
    if element_name in object1 and element_name in object2:
        element1_s = pd.Series(object1[element_name])
        element2_s = pd.Series(object2[element_name])
        #print(element1_s)
        #print(element2_s)
        e1e2_compare = element1_s.compare(element2_s, result_names=(filename1, filename2))
        if not e1e2_compare.empty: 
            return e1e2_compare
    return pd.DataFrame()

def diff_dict(filename1, filename2, object1, object2):
    object_pds = []
    object_indexes = []
    index_name = ""
    for object in [object1, object2]:
        rows = {}
        index_row = []
        for element in object:
            for key in element:
                if "id" in key:
                    index_name = key
                    index_row.append(element[key])
                elif key in rows:
                    rows[key].append(element[key])
                else:
                    rows[key] = [element[key]]
        object_index = pd.Index(index_row, name=index_name)
        object_indexes.append(object_index)
        object_pds.append(pd.DataFrame(rows, index=object_index))
    numcols1 = len(object_pds[0].columns)
    numcols2 = len(object_pds[0].columns)
    if debug:
        print("-"*60)
        print(object_pds[0])
        print("-"*30)
        print(object_pds[1])
        print()
    o1idx_diff = object_indexes[0].difference(object_indexes[1])
    o2idx_diff = object_indexes[1].difference(object_indexes[0])
    if debug:
        print("-"*60)
        print(o1idx_diff)
        print(o2idx_diff)
    if not o1idx_diff.empty:
        new_rows = []
        new_idx = []
        for i in o1idx_diff:
            row = []
            for c in range(numcols1):
                row.append("")
            new_rows.append(row)
            new_idx.append(i)
        columns = object_pds[0].columns
        new_rows_pd = pd.DataFrame(new_rows, index=new_idx, columns=columns)
        object_pds[1] = pd.concat([object_pds[1], new_rows_pd])
    if not o2idx_diff.empty:
        new_rows = []
        new_idx = []
        for i in o2idx_diff:
            row = []
            for c in range(numcols2):
                row.append("")
            new_rows.append(row)
            new_idx.append(i)
        columns = object_pds[0].columns
        new_rows_pd = pd.DataFrame(new_rows, index=new_idx, columns=columns)
        object_pds[0] = pd.concat([object_pds[0], new_rows_pd])
    object_pds[0].sort_index(inplace=True)
    object_pds[1].sort_index(inplace=True)
    if debug:
        print("-"*60)
        print(object_pds[0])
        print("-"*30)
        print(object_pds[1])
        print()
    e1e2_compare = object_pds[0].compare(object_pds[1], result_names=(filename1, filename2))
    return e1e2_compare

def diff_fight_techniques(filename1, filename2, fight1, fight2):
    if "techniques" in fight1:
        object_class = "techniques"
        if object_class in fight2:
            for object1 in fight1[object_class]:
                fgtid = object1["id"]
                object2 = find_fgtid(fight2, fgtid)
                if object2:
                    all_df = []
                    print(f"## diff between {filename1} and {filename2} in {fgtid}\n\n")
                    for element in ["name", "bluff", "access-required", "architecture-segment", "description", "platforms", "status"]:
                        element_df = diff_str(filename1, filename2, object1, object2, element)
                        if not element_df.empty:
                            all_df.append(element_df)
                    if all_df:
                        change_df = pd.concat(all_df)
                        diff_table = tabulate(change_df, headers="keys", tablefmt="github")
                        diff_table = diff_table.replace('\x0d\x0a', '  ')
                        print(diff_table)
                        print("\n\n"+"-"*3+"\n\n\n")
                    # for element in ["references", "tactics"]:
                    #     change_df = diff_list(filename1, filename2, object1, object2, element)
                    #     if not change_df.empty:
                    #         diff_table = tabulate(change_df, headers="keys", tablefmt="github")
                    #         diff_table = diff_table.replace('\x0d\x0a', '  ')
                    #         print(diff_table)
                    #         print("\n\n"+"-"*3+"\n\n\n")
                    for element in ["detections", "mitigations"]:
                        if element in object1 and element in object2:
                            change_df = diff_dict(filename1, filename2, object1[element], object2[element])
                            if not change_df.empty:
                                diff_table = tabulate(change_df, headers="keys", tablefmt="github")
                                diff_table = diff_table.replace('\x0d\x0a', '  ')
                                print(diff_table)
                                print("\n\n"+"-"*3+"\n\n\n")

if __name__ == "__main__":
    args = parse_args()
    fight1 = read_yaml(args.file1)
    fight2 = read_yaml(args.file2)
    diff_fight_techniques(args.file1, args.file2, fight1, fight2)
